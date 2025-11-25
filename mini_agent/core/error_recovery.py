#!/usr/bin/env python3
"""
Error Recovery and Resilience System
===================================

Provides comprehensive error recovery including circuit breakers, retry logic,
and fallback mechanisms for fault-tolerant task execution.

Author: Mini-Agent Enhancement Project
Date: 2025-11-25
"""

import asyncio
import hashlib
import json
import logging
import random
import time
from dataclasses import dataclass, field
from enum import Enum
from functools import wraps
from typing import Dict, Any, Optional, List, Callable, Union
import traceback

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """Classification of error types for recovery strategies"""
    TRANSIENT = "transient"          # Network, timeout, temporary issues
    PERSISTENT = "persistent"        # Auth, permission, data issues
    CATASTROPHIC = "catastrophic"    # System overload, security breach
    BUSINESS_LOGIC = "business_logic" # Invalid data, missing requirements

class RecoveryStrategy(Enum):
    """Recovery strategy types"""
    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    ESCALATE = "escalate"
    IGNORE = "ignore"

class CircuitBreakerState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, block requests
    HALF_OPEN = "half_open" # Testing recovery

@dataclass
class ErrorContext:
    """Context information for error analysis"""
    error_type: ErrorType
    operation: str
    component: str
    timestamp: float
    error_message: str
    stack_trace: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    user_context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RetryConfig:
    """Configuration for retry logic"""
    max_attempts: int = 3
    initial_delay: float = 1.0
    max_delay: float = 60.0
    backoff_factor: float = 2.0
    jitter: bool = True
    retry_on_types: List[ErrorType] = field(default_factory=lambda: [ErrorType.TRANSIENT])

@dataclass
class CircuitBreakerConfig:
    """Configuration for circuit breaker"""
    failure_threshold: int = 5
    timeout: float = 60.0
    success_threshold: int = 3  # For half-open state
    expected_exception_types: List[type] = field(default_factory=list)

class CircuitBreaker:
    """Circuit breaker implementation for fault tolerance"""
    
    def __init__(self, name: str, config: CircuitBreakerConfig):
        self.name = name
        self.config = config
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = 0
        self.state = CircuitBreakerState.CLOSED
        
        # Statistics
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        logger.info(f"Circuit breaker '{name}' initialized")
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        self.total_requests += 1
        
        if not await self._should_allow_request():
            raise Exception(f"Circuit breaker '{self.name}' is OPEN")
        
        try:
            result = await func(*args, **kwargs)
            await self._on_success()
            return result
            
        except Exception as e:
            await self._on_failure(e)
            raise e
    
    async def _should_allow_request(self) -> bool:
        """Check if request should be allowed based on current state"""
        current_time = time.time()
        
        if self.state == CircuitBreakerState.CLOSED:
            return True
        
        elif self.state == CircuitBreakerState.OPEN:
            # Check if timeout has elapsed for trying half-open
            if current_time - self.last_failure_time >= self.config.timeout:
                self.state = CircuitBreakerState.HALF_OPEN
                self.success_count = 0
                logger.info(f"Circuit breaker '{self.name}' moving to HALF_OPEN state")
                return True
            return False
        
        elif self.state == CircuitBreakerState.HALF_OPEN:
            return True
        
        return False
    
    async def _on_success(self):
        """Handle successful operation"""
        self.failure_count = 0
        self.successful_requests += 1
        
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitBreakerState.CLOSED
                logger.info(f"Circuit breaker '{self.name}' recovered and CLOSED")
        
        logger.debug(f"Circuit breaker '{self.name}' success (state: {self.state.value})")
    
    async def _on_failure(self, exception: Exception):
        """Handle failed operation"""
        self.failure_count += 1
        self.failed_requests += 1
        self.last_failure_time = time.time()
        
        # Check if we should open the circuit
        if self.state == CircuitBreakerState.CLOSED:
            if self.failure_count >= self.config.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                logger.warning(f"Circuit breaker '{self.name}' opened due to {self.failure_count} failures")
        
        elif self.state == CircuitBreakerState.HALF_OPEN:
            # Any failure in half-open state opens the circuit again
            self.state = CircuitBreakerState.OPEN
            logger.warning(f"Circuit breaker '{self.name}' reopened due to failure in half-open state")
        
        logger.debug(f"Circuit breaker '{self.name}' failure (state: {self.state.value})")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get circuit breaker statistics"""
        return {
            'name': self.name,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'total_requests': self.total_requests,
            'success_rate': (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0,
            'failure_rate': (self.failed_requests / self.total_requests * 100) if self.total_requests > 0 else 0
        }

class RetryManager:
    """Manages retry logic with exponential backoff and jitter"""
    
    def __init__(self, default_config: RetryConfig):
        self.default_config = default_config
        self.retry_strategies = self._initialize_retry_strategies()
        self.retry_statistics = {
            'total_retries': 0,
            'successful_retries': 0,
            'failed_retries': 0,
            'average_delay': 0.0
        }
    
    def _initialize_retry_strategies(self) -> Dict[ErrorType, RetryConfig]:
        """Initialize retry strategies for different error types"""
        return {
            ErrorType.TRANSIENT: RetryConfig(
                max_attempts=5,
                initial_delay=1.0,
                max_delay=60.0,
                backoff_factor=2.0,
                jitter=True,
                retry_on_types=[ErrorType.TRANSIENT]
            ),
            ErrorType.PERSISTENT: RetryConfig(
                max_attempts=2,
                initial_delay=5.0,
                max_delay=30.0,
                backoff_factor=1.5,
                jitter=True,
                retry_on_types=[ErrorType.PERSISTENT]
            ),
            ErrorType.BUSINESS_LOGIC: RetryConfig(
                max_attempts=1,
                initial_delay=0.0,
                max_delay=0.0,
                backoff_factor=1.0,
                jitter=False,
                retry_on_types=[ErrorType.BUSINESS_LOGIC]
            ),
            ErrorType.CATASTROPHIC: RetryConfig(
                max_attempts=0,
                initial_delay=0.0,
                max_delay=0.0,
                backoff_factor=1.0,
                jitter=False,
                retry_on_types=[]
            )
        }
    
    async def execute_with_retry(self, func: Callable, error_context: ErrorContext, *args, **kwargs) -> Any:
        """Execute function with retry logic"""
        retry_config = self.retry_strategies.get(error_context.error_type, self.default_config)
        
        # Check if this error type should be retried
        if error_context.error_type not in retry_config.retry_on_types:
            logger.info(f"Not retrying {error_context.error_type.value} error")
            raise Exception(error_context.error_message)
        
        last_exception = None
        total_delay = 0.0
        
        for attempt in range(retry_config.max_attempts):
            try:
                result = await func(*args, **kwargs)
                
                # Record successful retry
                self.retry_statistics['successful_retries'] += 1
                if attempt > 0:
                    self.retry_statistics['total_retries'] += 1
                    self.retry_statistics['average_delay'] = total_delay / self.retry_statistics['total_retries']
                
                logger.info(f"Function succeeded on attempt {attempt + 1}")
                return result
                
            except Exception as e:
                last_exception = e
                
                if attempt < retry_config.max_attempts - 1:
                    # Calculate delay for next retry
                    delay = self._calculate_delay(attempt, retry_config)
                    total_delay += delay
                    
                    logger.warning(f"Retry attempt {attempt + 1} for {error_context.operation}: {e} (delay: {delay:.1f}s)")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"All {retry_config.max_attempts} retry attempts failed for {error_context.operation}")
        
        # All retries failed
        self.retry_statistics['failed_retries'] += 1
        raise last_exception
    
    def _calculate_delay(self, attempt: int, config: RetryConfig) -> float:
        """Calculate delay for retry attempt with exponential backoff and jitter"""
        delay = config.initial_delay * (config.backoff_factor ** attempt)
        delay = min(delay, config.max_delay)
        
        # Add jitter to prevent thundering herd problem
        if config.jitter:
            # Use hash-based jitter for deterministic results
            jitter_range = delay * 0.1  # 10% jitter
            hash_value = int(hashlib.md5(f"{time.time()}_{attempt}".encode()).hexdigest(), 16)
            jitter = (hash_value % 100) / 100.0 * jitter_range * 2 - jitter_range
            delay += jitter
        
        return max(0.1, delay)  # Minimum 100ms delay

class FallbackHandler:
    """Handles fallback strategies for failed operations"""
    
    def __init__(self):
        self.fallback_strategies: Dict[str, Callable] = {}
        self.fallback_statistics = {
            'total_fallbacks': 0,
            'successful_fallbacks': 0,
            'failed_fallbacks': 0
        }
        
        # Register default fallback strategies
        self._register_default_fallbacks()
    
    def register_fallback(self, operation: str, fallback_func: Callable):
        """Register fallback function for an operation"""
        self.fallback_strategies[operation] = fallback_func
        logger.info(f"Registered fallback for operation: {operation}")
    
    async def handle_fallback(self, operation: str, error: Exception, context: Dict[str, Any]) -> Optional[Any]:
        """Execute fallback for failed operation"""
        if operation not in self.fallback_strategies:
            logger.warning(f"No fallback registered for operation: {operation}")
            return None
        
        try:
            self.fallback_statistics['total_fallbacks'] += 1
            
            fallback_func = self.fallback_strategies[operation]
            result = await fallback_func(error, context)
            
            self.fallback_statistics['successful_fallbacks'] += 1
            logger.info(f"Fallback executed successfully for operation: {operation}")
            
            return result
            
        except Exception as fallback_error:
            self.fallback_statistics['failed_fallbacks'] += 1
            logger.error(f"Fallback failed for operation {operation}: {fallback_error}")
            return None
    
    def _register_default_fallbacks(self):
        """Register default fallback strategies"""
        
        async def web_search_fallback(error: Exception, context: Dict[str, Any]):
            """Fallback for web search failures"""
            logger.warning("Using fallback for web search")
            return {
                'error': 'Search service temporarily unavailable',
                'fallback': True,
                'message': 'Web search is currently unavailable. Please try again later.',
                'suggestion': 'Check your internet connection and try again in a few moments.'
            }
        
        async def api_call_fallback(error: Exception, context: Dict[str, Any]):
            """Fallback for API call failures"""
            logger.warning("Using fallback for API call")
            return {
                'error': 'API service temporarily unavailable',
                'fallback': True,
                'message': 'The requested service is currently unavailable.',
                'suggestion': 'Please try again later or contact support if the issue persists.'
            }
        
        async def database_fallback(error: Exception, context: Dict[str, Any]):
            """Fallback for database failures"""
            logger.warning("Using fallback for database operation")
            return {
                'error': 'Database temporarily unavailable',
                'fallback': True,
                'message': 'Database operations are currently unavailable.',
                'suggestion': 'Please try again later. Your data has been preserved.'
            }
        
        async def file_operation_fallback(error: Exception, context: Dict[str, Any]):
            """Fallback for file operation failures"""
            logger.warning("Using fallback for file operation")
            return {
                'error': 'File operation failed',
                'fallback': True,
                'message': 'Unable to complete the requested file operation.',
                'suggestion': 'Please check file permissions and try again.'
            }
        
        async def llm_generation_fallback(error: Exception, context: Dict[str, Any]):
            """Fallback for LLM generation failures"""
            logger.warning("Using fallback for LLM generation")
            # Create a simple error response string that the agent can handle
            error_msg = f"Error: LLM service temporarily unavailable. {str(error)}"
            return error_msg
        
        # Register fallbacks
        self.register_fallback("web_search", web_search_fallback)
        self.register_fallback("api_call", api_call_fallback)
        self.register_fallback("database_operation", database_fallback)
        self.register_fallback("file_operation", file_operation_fallback)
        self.register_fallback("llm_generation", llm_generation_fallback)

class ErrorAnalyzer:
    """Analyzes errors to determine type and appropriate recovery strategy"""
    
    def __init__(self):
        self.error_patterns = self._initialize_error_patterns()
    
    def _initialize_error_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize error pattern recognition"""
        return {
            # Network and connection errors (Transient)
            'connection_timeout': {
                'error_types': [ErrorType.TRANSIENT],
                'patterns': ['timeout', 'timed out', 'connection.*timeout'],
                'recovery': RecoveryStrategy.RETRY
            },
            'network_error': {
                'error_types': [ErrorType.TRANSIENT],
                'patterns': ['network.*error', 'connection.*refused', 'connection.*reset'],
                'recovery': RecoveryStrategy.RETRY
            },
            'rate_limit': {
                'error_types': [ErrorType.TRANSIENT],
                'patterns': ['rate.*limit', 'too.*many.*requests', 'quota.*exceeded'],
                'recovery': RecoveryStrategy.RETRY
            },
            
            # Authentication and authorization (Persistent)
            'authentication_error': {
                'error_types': [ErrorType.PERSISTENT],
                'patterns': ['unauthorized', 'authentication.*failed', 'invalid.*token'],
                'recovery': RecoveryStrategy.ESCALATE
            },
            'permission_error': {
                'error_types': [ErrorType.PERSISTENT],
                'patterns': ['permission.*denied', 'access.*forbidden', 'insufficient.*privileges'],
                'recovery': RecoveryStrategy.ESCALATE
            },
            
            # System overload (Catastrophic)
            'system_overload': {
                'error_types': [ErrorType.CATASTROPHIC],
                'patterns': ['system.*overload', 'out.*of.*memory', 'resource.*exhausted'],
                'recovery': RecoveryStrategy.CIRCUIT_BREAKER
            },
            'security_breach': {
                'error_types': [ErrorType.CATASTROPHIC],
                'patterns': ['security.*violation', 'unauthorized.*access', 'attack.*detected'],
                'recovery': RecoveryStrategy.ESCALATE
            },
            
            # Business logic errors (Business Logic)
            'invalid_data': {
                'error_types': [ErrorType.BUSINESS_LOGIC],
                'patterns': ['invalid.*input', 'validation.*failed', 'bad.*request'],
                'recovery': RecoveryStrategy.IGNORE
            },
            'missing_requirements': {
                'error_types': [ErrorType.BUSINESS_LOGIC],
                'patterns': ['missing.*parameter', 'required.*field', 'incomplete.*data'],
                'recovery': RecoveryStrategy.IGNORE
            }
        }
    
    async def analyze_error(self, error: Exception, context: Dict[str, Any]) -> ErrorContext:
        """Analyze error and determine type and strategy"""
        error_message = str(error)
        stack_trace = traceback.format_exc()
        
        # Determine error type
        error_type = self._classify_error(error_message)
        
        # Determine recovery strategy
        recovery_strategy = self._determine_recovery_strategy(error_message, error_type)
        
        error_context = ErrorContext(
            error_type=error_type,
            operation=context.get('operation', 'unknown'),
            component=context.get('component', 'unknown'),
            timestamp=time.time(),
            error_message=error_message,
            stack_trace=stack_trace,
            metadata=context.get('metadata', {}),
            user_context=context.get('user_context', {})
        )
        
        logger.debug(f"Analyzed error: {error_type.value} -> {recovery_strategy.value}")
        return error_context
    
    def _classify_error(self, error_message: str) -> ErrorType:
        """Classify error based on message patterns"""
        error_lower = error_message.lower()
        
        for pattern_name, pattern_info in self.error_patterns.items():
            for pattern in pattern_info['patterns']:
                if pattern.lower() in error_lower:
                    # Return the first error type in the pattern
                    return pattern_info['error_types'][0]
        
        # Default classification based on common error indicators
        if any(keyword in error_lower for keyword in ['timeout', 'connection', 'network']):
            return ErrorType.TRANSIENT
        elif any(keyword in error_lower for keyword in ['unauthorized', 'forbidden', 'permission']):
            return ErrorType.PERSISTENT
        elif any(keyword in error_lower for keyword in ['overload', 'memory', 'resource']):
            return ErrorType.CATASTROPHIC
        else:
            return ErrorType.BUSINESS_LOGIC
    
    def _determine_recovery_strategy(self, error_message: str, error_type: ErrorType) -> RecoveryStrategy:
        """Determine appropriate recovery strategy for error"""
        error_lower = error_message.lower()
        
        for pattern_name, pattern_info in self.error_patterns.items():
            for pattern in pattern_info['patterns']:
                if pattern.lower() in error_lower:
                    return pattern_info['recovery']
        
        # Default strategies based on error type
        default_strategies = {
            ErrorType.TRANSIENT: RecoveryStrategy.RETRY,
            ErrorType.PERSISTENT: RecoveryStrategy.ESCALATE,
            ErrorType.CATASTROPHIC: RecoveryStrategy.CIRCUIT_BREAKER,
            ErrorType.BUSINESS_LOGIC: RecoveryStrategy.IGNORE
        }
        
        return default_strategies.get(error_type, RecoveryStrategy.RETRY)

class ErrorRecoveryOrchestrator:
    """Orchestrates error recovery across the system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.retry_manager = RetryManager(RetryConfig())
        self.fallback_handler = FallbackHandler()
        self.error_analyzer = ErrorAnalyzer()
        
        # Statistics
        self.recovery_statistics = {
            'total_recoveries': 0,
            'successful_recoveries': 0,
            'failed_recoveries': 0,
            'circuit_breaker_trips': 0,
            'fallback_executions': 0
        }
        
        logger.info("Error recovery orchestrator initialized")
    
    async def execute_with_recovery(self, operation: str, func: Callable, context: Dict[str, Any], *args, **kwargs) -> Any:
        """Execute operation with comprehensive error recovery"""
        
        # Get or create circuit breaker for this operation
        circuit_breaker = await self._get_circuit_breaker(operation)
        
        try:
            # Create error context for the function call
            expected_error_types = await self._analyze_operation_errors(operation)
            error_context = ErrorContext(
                error_type=expected_error_types[0] if expected_error_types else ErrorType.TRANSIENT,
                operation=operation,
                component=context.get('component', 'unknown'),
                timestamp=time.time(),
                error_message="",
                stack_trace="",
                metadata=context
            )
            
            # Execute with circuit breaker protection
            async def execute_with_protection():
                # First execute with retry
                try:
                    return await self.retry_manager.execute_with_retry(func, error_context, *args, **kwargs)
                except Exception:
                    # Retry failed, raise the exception to trigger fallback
                    raise
            
            result = await circuit_breaker.call(execute_with_protection)
            
            # Record successful recovery
            self.recovery_statistics['successful_recoveries'] += 1
            return result
                
        except Exception as e:
            # Analyze the actual error
            error_context = await self.error_analyzer.analyze_error(e, context)
            
            logger.error(f"Operation {operation} failed: {error_context.error_message}")
            
            # Try fallback
            fallback_result = await self.fallback_handler.handle_fallback(operation, e, context)
            
            if fallback_result is not None:
                self.recovery_statistics['fallback_executions'] += 1
                return fallback_result
            else:
                # No fallback available, escalate error
                self.recovery_statistics['failed_recoveries'] += 1
                raise e
            
        finally:
            self.recovery_statistics['total_recoveries'] += 1
    
    async def _get_circuit_breaker(self, operation: str) -> CircuitBreaker:
        """Get or create circuit breaker for operation"""
        if operation not in self.circuit_breakers:
            config = CircuitBreakerConfig(
                failure_threshold=self.config.get('failure_threshold', 5),
                timeout=self.config.get('circuit_timeout', 60)
            )
            
            self.circuit_breakers[operation] = CircuitBreaker(operation, config)
        
        return self.circuit_breakers[operation]
    
    async def _analyze_operation_errors(self, operation: str) -> List[ErrorType]:
        """Analyze operation to predict likely error types"""
        # This is a simplified analysis - in practice, you'd have more sophisticated patterns
        error_patterns = {
            'web_search': [ErrorType.TRANSIENT, ErrorType.PERSISTENT],
            'api_call': [ErrorType.TRANSIENT, ErrorType.PERSISTENT],
            'database_operation': [ErrorType.TRANSIENT, ErrorType.PERSISTENT],
            'file_operation': [ErrorType.PERSISTENT, ErrorType.CATASTROPHIC],
            'llm_call': [ErrorType.TRANSIENT, ErrorType.CATASTROPHIC],
            'llm_generation': [ErrorType.TRANSIENT, ErrorType.CATASTROPHIC],
            'computation': [ErrorType.TRANSIENT, ErrorType.CATASTROPHIC]
        }
        
        for pattern, error_types in error_patterns.items():
            if pattern in operation:
                return error_types
        
        return [ErrorType.TRANSIENT]  # Default to transient errors
    
    def get_recovery_status(self) -> Dict[str, Any]:
        """Get error recovery system status"""
        
        circuit_breaker_stats = {
            name: cb.get_stats() 
            for name, cb in self.circuit_breakers.items()
        }
        
        return {
            'circuit_breakers': circuit_breaker_stats,
            'recovery_statistics': self.recovery_statistics,
            'retry_statistics': self.retry_manager.retry_statistics,
            'fallback_statistics': self.fallback_handler.fallback_statistics,
            'total_circuit_breakers': len(self.circuit_breakers),
            'active_circuit_breakers': len([cb for cb in self.circuit_breakers.values() if cb.state != CircuitBreakerState.CLOSED])
        }

# Decorator for easy integration
def with_error_recovery(operation: str, component: str = "unknown"):
    """Decorator for adding error recovery to functions"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # In practice, this would use a global recovery orchestrator instance
            # For now, we'll create a simple implementation
            recovery_orchestrator = get_recovery_orchestrator()  # Placeholder
            
            context = {
                'operation': operation,
                'component': component,
                'function': func.__name__
            }
            
            return await recovery_orchestrator.execute_with_recovery(
                operation, func, context, *args, **kwargs
            )
        return wrapper
    return decorator

# Global recovery orchestrator (placeholder - would be initialized properly in real implementation)
_recovery_orchestrator = None

def get_recovery_orchestrator() -> ErrorRecoveryOrchestrator:
    """Get global recovery orchestrator instance"""
    global _recovery_orchestrator
    if _recovery_orchestrator is None:
        _recovery_orchestrator = ErrorRecoveryOrchestrator({})
    return _recovery_orchestrator

# Export main classes
__all__ = [
    'ErrorRecoveryOrchestrator',
    'CircuitBreaker',
    'RetryManager', 
    'FallbackHandler',
    'ErrorAnalyzer',
    'ErrorContext',
    'ErrorType',
    'RecoveryStrategy',
    'CircuitBreakerState',
    'RetryConfig',
    'CircuitBreakerConfig',
    'with_error_recovery'
]
