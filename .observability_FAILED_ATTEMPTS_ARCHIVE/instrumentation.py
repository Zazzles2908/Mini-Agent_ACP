#!/usr/bin/env python3
"""
Mini-Agent Tool Instrumentation Wrapper
Automatically wraps tool calls with observability logging
"""

import os
import time
import functools
import inspect
from typing import Any, Callable, Dict, Optional, TypeVar, cast
from datetime import datetime, timezone

# Import our observability client
from client import MiniAgentObservability

# Type hint for generic functions
F = TypeVar('F', bound=Callable[..., Any])

class MiniAgentInstrumentation:
    """
    Provides instrumentation utilities for wrapping Mini-Agent tools
    with observability logging
    """
    
    def __init__(self, observability_client: Optional[MiniAgentObservability] = None):
        self.observability = observability_client or MiniAgentObservability()
        self.instrumentation_enabled = True
    
    def instrument_tool(self, 
                       tool_name: Optional[str] = None,
                       category: str = "core",
                       capture_input: bool = True,
                       capture_output: bool = True,
                       capture_error: bool = True) -> Callable[[F], F]:
        """
        Decorator to instrument tool functions with observability logging
        
        Args:
            tool_name: Name to use for the tool (defaults to function name)
            category: Tool category (core, file, mcp, document, skill)
            capture_input: Whether to capture and log function inputs
            capture_output: Whether to capture and log function outputs
            capture_error: Whether to capture and log errors
        """
        
        def decorator(func: F) -> F:
            actual_tool_name = tool_name or func.__name__
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.instrumentation_enabled:
                    return func(*args, **kwargs)
                
                start_time = datetime.now(timezone.utc)
                input_data = {}
                output_data = {}
                error_message = None
                success = True
                
                # Capture input data
                if capture_input:
                    try:
                        # Get function signature for better parameter names
                        sig = inspect.signature(func)
                        bound_args = sig.bind(*args, **kwargs)
                        bound_args.apply_defaults()
                        input_data = {
                            'function': actual_tool_name,
                            'args': dict(bound_args.arguments),
                            'args_count': len(args),
                            'kwargs_count': len(kwargs)
                        }
                    except Exception as e:
                        input_data = {'function': actual_tool_name, 'capture_error': str(e)}
                
                try:
                    # Execute the function
                    result = func(*args, **kwargs)
                    
                    # Capture output data
                    if capture_output:
                        try:
                            if isinstance(result, (dict, list, str, int, float, bool)):
                                output_data = {
                                    'result': result,
                                    'result_type': type(result).__name__
                                }
                            else:
                                output_data = {
                                    'result_type': type(result).__name__,
                                    'result_str': str(result)[:500]  # Truncate long results
                                }
                        except Exception as e:
                            output_data = {'capture_error': str(e)}
                    
                    return result
                    
                except Exception as e:
                    success = False
                    error_message = str(e)
                    
                    if capture_error:
                        output_data = {
                            'error': error_message,
                            'error_type': type(e).__name__
                        }
                    
                    # Re-raise the exception
                    raise
                
                finally:
                    # Always log the tool execution
                    try:
                        self.observability.log_tool_execution(
                            tool_name=actual_tool_name,
                            category=category,
                            input_data=input_data,
                            output_data=output_data,
                            success=success,
                            error_message=error_message,
                            start_time=start_time
                        )
                    except Exception as e:
                        # Don't let observability failures break the tool
                        print(f"Warning: Observability logging failed: {e}")
            
            return cast(F, wrapper)
        
        return decorator
    
    def instrument_class_methods(self, 
                                instance: Any,
                                category: str = "core",
                                method_pattern: Optional[str] = None) -> None:
        """
        Instrument all methods of a class instance
        
        Args:
            instance: Class instance to instrument
            category: Category for all instrumented methods
            method_pattern: Optional pattern to filter methods (e.g., "*tool*")
        """
        for attr_name in dir(instance):
            # Skip private attributes and built-ins
            if attr_name.startswith('_') or attr_name in ['__class__', '__dict__', '__module__']:
                continue
            
            attr = getattr(instance, attr_name)
            
            # Only instrument callable attributes (methods)
            if not callable(attr):
                continue
            
            # Apply pattern filter if specified
            if method_pattern:
                if '*' in method_pattern:
                    pattern = method_pattern.replace('*', '.*')
                    import re
                    if not re.match(pattern, attr_name):
                        continue
                elif method_pattern not in attr_name:
                    continue
            
            # Instrument the method
            try:
                instrumented_method = self.instrument_tool(
                    tool_name=f"{instance.__class__.__name__}.{attr_name}",
                    category=category
                )(attr)
                setattr(instance, attr_name, instrumented_method)
                print(f"[OK] Instrumented: {instance.__class__.__name__}.{attr_name}")
            except Exception as e:
                print(f"[WARN] Failed to instrument {instance.__class__.__name__}.{attr_name}: {e}")
    
    def start_session(self) -> None:
        """Start a new observability session"""
        if not self.observability.session_id:
            self.observability = MiniAgentObservability()
    
    def end_session(self) -> None:
        """End the current observability session"""
        if self.observability:
            self.observability.close_session()
    
    def log_performance(self, metric_type: str, value: float, unit: str) -> None:
        """Log a performance metric"""
        if self.observability:
            self.observability.log_performance_metric(metric_type, value, unit)
    
    def log_decision(self, decision_type: str, considered: list, selected: str, reasoning: str, confidence: float = None) -> None:
        """Log an agent decision"""
        if self.observability:
            self.observability.log_agent_decision(decision_type, considered, selected, reasoning, confidence)
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable instrumentation"""
        self.instrumentation_enabled = enabled

# Global instrumentation instance
_instrumentation = MiniAgentInstrumentation()

# Convenience functions
def instrument_tool(tool_name: Optional[str] = None, category: str = "core") -> Callable[[F], F]:
    """Decorator to instrument a tool function"""
    return _instrumentation.instrument_tool(tool_name, category)

def instrument_class(instance: Any, category: str = "core", method_pattern: Optional[str] = None) -> None:
    """Instrument all methods of a class instance"""
    return _instrumentation.instrument_class_methods(instance, category, method_pattern)

def log_performance(metric_type: str, value: float, unit: str) -> None:
    """Log a performance metric"""
    return _instrumentation.log_performance(metric_type, value, unit)

def log_decision(decision_type: str, considered: list, selected: str, reasoning: str, confidence: float = None) -> None:
    """Log an agent decision"""
    return _instrumentation.log_decision(decision_type, considered, selected, reasoning, confidence)

def set_instrumentation_enabled(enabled: bool) -> None:
    """Enable or disable instrumentation globally"""
    return _instrumentation.set_enabled(enabled)

# Example usage
if __name__ == "__main__":
    print("Mini-Agent Tool Instrumentation Test")
    print("=" * 50)
    
    # Example 1: Instrument a simple function
    @instrument_tool(category="file")
    def read_file(file_path: str, mode: str = "r"):
        """Example file reading function"""
        # Simulate file reading
        time.sleep(0.1)  # Simulate I/O delay
        return {"content": f"Content of {file_path}", "lines": 42}
    
    # Example 2: Instrument a class
    class FileManager:
        def __init__(self):
            self.files_opened = 0
        
        @instrument_tool(category="file")
        def open_file(self, path: str):
            self.files_opened += 1
            time.sleep(0.05)
            return {"handle": f"file_{self.files_opened}", "path": path}
        
        @instrument_tool(category="file")  
        def close_file(self, handle: str):
            time.sleep(0.01)
            return {"closed": True, "handle": handle}
    
    # Test instrumentation
    print("\nTesting function instrumentation...")
    result = read_file("/test/document.txt", "r")
    print(f"Function result: {result}")
    
    print("\nTesting class instrumentation...")
    file_manager = FileManager()
    instrument_class(file_manager, category="file")
    
    file1 = file_manager.open_file("/data/file1.txt")
    file2 = file_manager.open_file("/data/file2.txt")
    closed = file_manager.close_file(file1["handle"])
    
    print(f"Class results: opened={file_manager.files_opened}, closed={closed}")
    
    # Test performance logging
    print("\nTesting performance logging...")
    log_performance("memory_usage", 256.7, "MB")
    log_performance("cpu_usage", 15.3, "%")
    
    # Test decision logging
    print("\nTesting decision logging...")
    log_decision(
        decision_type="tool_selection",
        considered=["read_file", "bash.cat", "smart_file_query"],
        selected="read_file",
        reasoning="File reading requires direct file access",
        confidence=0.9
    )
    
    print("\n✅ Instrumentation test completed!")
    print("Check Langfuse and Supabase for logged data.")
