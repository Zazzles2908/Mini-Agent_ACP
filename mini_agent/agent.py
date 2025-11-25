"""Enhanced Agent implementation with Phase 1 components."""

import json
import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

import tiktoken

from .llm.llm_wrapper import LLMClient
from .logger import AgentLogger
from .schema import Message
from .tools.base import Tool, ToolResult
from .utils import calculate_display_width
from .core.context_overflow_prevention import get_context_manager

# Phase 1 Integration: Task Orchestration, Session Management, Error Recovery
from .orchestration.task_orchestrator import TaskOrchestrator, ComplexityLevel
from .session.session_manager import SessionLifecycleManager
from .core.error_recovery import ErrorRecoveryOrchestrator

logger = logging.getLogger(__name__)


# ANSI color codes
class Colors:
    """Terminal color definitions"""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


# Icon replacements for compatibility
ICON_WARNING = "⚠"
ICON_SUCCESS = "✅"
ICON_ERROR = "❌"
ICON_INFO = "ℹ"
ICON_STEP = "➤"
ICON_THINKING = "💭"
ICON_ASSISTANT = "🤖"
ICON_TOOL = "🔧"
ICON_RESULT = "📋"
ICON_VALIDATION = "🔍"
ICON_QUALITY = "⭐"
ICON_FEEDBACK = "💬"


class Agent:
    """Enhanced agent with task orchestration, session management, and error recovery."""

    def __init__(
        self,
        llm_client: LLMClient,
        system_prompt: str,
        tools: list[Tool],
        max_steps: int = 50,
        workspace_dir: str = "./workspace",
        token_limit: int = 200000,  # Summary triggered when tokens exceed this value (updated for 200K context)
        config: Dict[str, Any] = None,
    ):
        self.llm = llm_client
        self.tools = {tool.name: tool for tool in tools}
        self.max_steps = max_steps
        self.token_limit = token_limit
        self.workspace_dir = Path(workspace_dir)
        self.config = config or {}

        # Ensure workspace exists
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

        # Inject workspace information into system prompt if not already present
        if "Current Workspace" not in system_prompt:
            workspace_info = f"\n\n## Current Workspace\nYou are currently working in: `{self.workspace_dir.absolute()}`\nAll relative paths will be resolved relative to this directory."
            system_prompt = system_prompt + workspace_info

        self.system_prompt = system_prompt

        # Initialize message history
        self.messages: list[Message] = [Message(role="system", content=system_prompt)]

        # Initialize logger
        self.logger = AgentLogger()
        
        # Initialize context overflow prevention
        try:
            self.context_manager = get_context_manager()
        except Exception as e:
            print(f"Warning: Failed to initialize context overflow prevention: {e}")
            self.context_manager = None

        # Phase 1 Integration: Initialize enhanced components
        self._initialize_enhanced_components()

    def _initialize_enhanced_components(self):
        """Initialize Phase 1 enhanced components"""
        
        # Task Orchestration System
        if self.config.get('orchestration', {}).get('enabled', True):
            try:
                self.task_orchestrator = TaskOrchestrator(
                    config=self.config.get('orchestration', {}),
                    llm_client=self.llm,
                    agent_instance=self
                )
                print(f"{Colors.BRIGHT_GREEN}[ORCHESTRATION] Task orchestration enabled{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.BRIGHT_YELLOW}[WARNING] Failed to initialize task orchestrator: {e}{Colors.RESET}")
                self.task_orchestrator = None
        else:
            self.task_orchestrator = None

        # Session Management System
        if self.config.get('session_management', {}).get('enabled', True):
            try:
                self.session_manager = SessionLifecycleManager(
                    config=self.config.get('session_management', {})
                )
                print(f"{Colors.BRIGHT_GREEN}[SESSION] Session management enabled{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.BRIGHT_YELLOW}[WARNING] Failed to initialize session manager: {e}{Colors.RESET}")
                self.session_manager = None
        else:
            self.session_manager = None

        # Error Recovery System
        if self.config.get('error_recovery', {}).get('enabled', True):
            try:
                self.error_recovery = ErrorRecoveryOrchestrator(
                    config=self.config.get('error_recovery', {})
                )
                print(f"{Colors.BRIGHT_GREEN}[RECOVERY] Error recovery enabled{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.BRIGHT_YELLOW}[WARNING] Failed to initialize error recovery: {e}{Colors.RESET}")
                self.error_recovery = None
        else:
            self.error_recovery = None

        # Current session for the agent
        self.current_session = None

        logger.info("Enhanced agent components initialized successfully")

    def add_user_message(self, content: str):
        """Add a user message to history."""
        self.messages.append(Message(role="user", content=content))

    def _estimate_tokens(self) -> int:
        """Accurately calculate token count for message history using tiktoken

        Uses cl100k_base encoder (GLM-4.6 (via Z.AI)/MiniMax-M2/M2 compatible)
        """
        try:
            # Use cl100k_base encoder (used by GLM-4.6 (via Z.AI) and most modern models)
            encoding = tiktoken.get_encoding("cl100k_base")
        except Exception:
            # Fallback: if tiktoken initialization fails, use simple estimation
            return self._estimate_tokens_fallback()

        total_tokens = 0

        for msg in self.messages:
            # Count text content
            if isinstance(msg.content, str):
                total_tokens += len(encoding.encode(msg.content))
            elif isinstance(msg.content, list):
                for block in msg.content:
                    if isinstance(block, dict):
                        # Convert dict to string for calculation
                        total_tokens += len(encoding.encode(str(block)))

            # Count thinking
            if msg.thinking:
                total_tokens += len(encoding.encode(msg.thinking))

            # Count tool_calls
            if msg.tool_calls:
                total_tokens += len(encoding.encode(str(msg.tool_calls)))

            # Metadata overhead per message (approximately 4 tokens)
            total_tokens += 4

        return total_tokens

    def _estimate_tokens_fallback(self) -> int:
        """Fallback token estimation method (when tiktoken is unavailable)"""
        total_chars = 0
        for msg in self.messages:
            if isinstance(msg.content, str):
                total_chars += len(msg.content)
            elif isinstance(msg.content, list):
                for block in msg.content:
                    if isinstance(block, dict):
                        total_chars += len(str(block))

            if msg.thinking:
                total_chars += len(msg.thinking)

            if msg.tool_calls:
                total_chars += len(str(msg.tool_calls))

        # Rough estimation: average 2.5 characters = 1 token
        return int(total_chars / 2.5)

    async def _summarize_messages(self):
        """Message history summarization: summarize conversations between user messages when tokens exceed limit

        Strategy (Agent mode):
        - Keep all user messages (these are user intents)
        - Summarize content between each user-user pair (agent execution process)
        - If last round is still executing (has agent/tool messages but no next user), also summarize
        - Structure: system -> user1 -> summary1 -> user2 -> summary2 -> user3 -> summary3 (if executing)
        """
        estimated_tokens = self._estimate_tokens()

        # If not exceeded, no summary needed
        if estimated_tokens <= self.token_limit:
            return

        print(f"\n{Colors.BRIGHT_YELLOW}[SCORE] Token estimate: {estimated_tokens}/{self.token_limit}{Colors.RESET}")
        print(f"{Colors.BRIGHT_YELLOW}[SUMMARIZE] Triggering message history summarization...{Colors.RESET}")

        # Find all user message indices (skip system prompt)
        user_indices = [i for i, msg in enumerate(self.messages) if msg.role == "user" and i > 0]

        # Need at least 1 user message to perform summary
        if len(user_indices) < 1:
            print(f"{Colors.BRIGHT_YELLOW}[ISSUE]  Insufficient messages, cannot summarize{Colors.RESET}")
            return

        # Build new message list
        new_messages = [self.messages[0]]  # Keep system prompt
        summary_count = 0

        # Iterate through each user message and summarize the execution process after it
        for i, user_idx in enumerate(user_indices):
            # Add current user message
            new_messages.append(self.messages[user_idx])

            # Determine message range to summarize
            # If last user, go to end of message list; otherwise to before next user
            if i < len(user_indices) - 1:
                next_user_idx = user_indices[i + 1]
            else:
                next_user_idx = len(self.messages)

            # Extract execution messages for this round
            execution_messages = self.messages[user_idx + 1 : next_user_idx]

            # If there are execution messages in this round, summarize them
            if execution_messages:
                summary_text = await self._create_summary(execution_messages, i + 1)
                if summary_text:
                    summary_message = Message(
                        role="user",
                        content=f"[Assistant Execution Summary]\n\n{summary_text}",
                    )
                    new_messages.append(summary_message)
                    summary_count += 1

        # Replace message list
        self.messages = new_messages

        new_tokens = self._estimate_tokens()
        print(f"{Colors.BRIGHT_GREEN}[SUCCESS] Summary completed, tokens reduced from {estimated_tokens} to {new_tokens}{Colors.RESET}")
        print(f"{Colors.DIM}  Structure: system + {len(user_indices)} user messages + {summary_count} summaries{Colors.RESET}")

    async def _create_summary(self, messages: list[Message], round_num: int) -> str:
        """Create summary for one execution round

        Args:
            messages: List of messages to summarize
            round_num: Round number

        Returns:
            Summary text
        """
        if not messages:
            return ""

        # Build summary content
        summary_content = f"Round {round_num} execution process:\n\n"
        for msg in messages:
            if msg.role == "assistant":
                content_text = msg.content if isinstance(msg.content, str) else str(msg.content)
                summary_content += f"Assistant: {content_text}\n"
                if msg.tool_calls:
                    tool_names = [tc.function.name for tc in msg.tool_calls]
                    summary_content += f"  {ICON_TOOL} Called tools: {', '.join(tool_names)}\n"
            elif msg.role == "tool":
                result_preview = msg.content if isinstance(msg.content, str) else str(msg.content)
                summary_content += f"  {ICON_RESULT} Tool returned: {result_preview}...\n"

        # Call LLM to generate concise summary
        try:
            summary_prompt = f"""Please provide a concise summary of the following Agent execution process:

{summary_content}

Requirements:
1. Focus on what tasks were completed and which tools were called
2. Keep key execution results and important findings
3. Be concise and clear, within 1000 words
4. Use English
5. Do not include "user" related content, only summarize the Agent's execution process"""

            summary_msg = Message(role="user", content=summary_prompt)
            response = await self.llm.generate(
                messages=[
                    Message(
                        role="system",
                        content="You are an assistant skilled at summarizing Agent execution processes.",
                    ),
                    summary_msg,
                ]
            )

            summary_text = response.content
            print(f"{Colors.BRIGHT_GREEN}[SUCCESS] Summary for round {round_num} generated successfully{Colors.RESET}")
            return summary_text

        except Exception as e:
            print(f"{Colors.BRIGHT_RED}{ICON_ERROR} Summary generation failed for round {round_num}: {e}{Colors.RESET}")
            # Use simple text summary on failure
            return summary_content

    async def _validate_task_completion(self, response) -> Optional[Dict[str, Any]]:
        """Validate task completion using QA validation system
        
        Args:
            response: The LLM response to validate
            
        Returns:
            Dict with validation results or None if validation system unavailable
        """
        # Check if QA validation tools are available
        try:
            from .tools import get_validation_tool
            ValidationTool = get_validation_tool()
            
            # Check if validation tool loaded successfully
            if ValidationTool is None:
                return None
            
            # Only run validation if tools are available and response is substantive
            if not response.content or len(response.content.strip()) < 20:
                return None
                
            # Create validation request from agent context
            validation_request = {
                "task_description": self._extract_task_from_context(),
                "claimed_deliverables": self._extract_claimed_deliverables(response.content),
                "requirements_checklist": self._extract_requirements_from_context(),
                "actual_files": self._get_actual_files_in_workspace(),
                "confidence_level": "medium",
                "validation_level": "moderate"
            }
            
            # Execute validation
            validation_tool = ValidationTool()
            result = await validation_tool.execute(
                task_description=validation_request["task_description"],
                claimed_deliverables=validation_request["claimed_deliverables"],
                requirements_checklist=validation_request["requirements_checklist"],
                actual_files=validation_request["actual_files"],
                confidence_level=validation_request["confidence_level"],
                validation_level=validation_request["validation_level"]
            )
            
            if result.success:
                return result.content
            else:
                print(f"{Colors.DIM}[ISSUE]  Validation failed: {result.error}{Colors.RESET}")
                return None
                
        except ImportError:
            # Validation tools not available
            return None
        except Exception as e:
            print(f"{Colors.DIM}[ISSUE]  Validation error: {e}{Colors.RESET}")
            return None

    def _extract_task_from_context(self) -> str:
        """Extract current task description from message context"""
        try:
            # Find the most recent user message for task context
            for msg in reversed(self.messages):
                if msg.role == "user":
                    content = msg.content
                    # If it's an execution summary, find the actual user request
                    if content.startswith("[Assistant Execution Summary]"):
                        continue
                    # Truncate if too long
                    return content[:500] + "..." if len(content) > 500 else content
            return "Task completion validation"
        except Exception:
            return "Task completion validation"

    def _extract_claimed_deliverables(self, response_content: str) -> List[str]:
        """Extract claimed deliverables from agent response"""
        try:
            deliverables = []
            
            # Look for common completion indicators
            completion_patterns = [
                r"created ([\w\/\-\.]+)",
                r"generated ([\w\/\-\.]+)",
                r"implemented ([\w\/\-\.]+)",
                r"built ([\w\/\-\.]+)",
                r"wrote ([\w\/\-\.]+)",
                r"produced ([\w\/\-\.]+)",
                r"completed ([\w\/\-\.]+)",
                r"delivered ([\w\/\-\.]+)",
            ]
            
            for pattern in completion_patterns:
                matches = re.findall(pattern, response_content, re.IGNORECASE)
                deliverables.extend(matches)
            
            # Remove duplicates and empty strings
            deliverables = [d.strip() for d in deliverables if d.strip()]
            return list(set(deliverables))[:10]  # Limit to 10 items
            
        except Exception:
            return []

    def _extract_requirements_from_context(self) -> List[str]:
        """Extract requirements from the current task context"""
        try:
            requirements = []
            
            # Look for requirements in recent user messages
            for msg in reversed(self.messages[-3:]):  # Check last 3 messages
                if msg.role == "user" and not msg.content.startswith("[Assistant Execution Summary]"):
                    content = msg.content
                    
                    # Look for requirement indicators
                    req_patterns = [
                        r"requirements?[:\s]*([^\n]+(?:\n[^\n]*)*?)(?=\n\n|\n$|$)",
                        r"must ([\w\s]+)",
                        r"should ([\w\s]+)",
                        r"need to ([\w\s]+)",
                        r"required ([\w\s]+)",
                    ]
                    
                    for pattern in req_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        requirements.extend([match.strip() for match in matches if match.strip()])
            
            return requirements[:5]  # Limit to 5 requirements
            
        except Exception:
            return []

    def _get_actual_files_in_workspace(self) -> List[str]:
        """Get list of actual files in the workspace"""
        try:
            files = []
            workspace_path = Path(self.workspace_dir)
            
            if workspace_path.exists():
                for file_path in workspace_path.rglob("*"):
                    if file_path.is_file() and not file_path.name.startswith('.'):
                        # Get relative path from workspace
                        try:
                            relative_path = file_path.relative_to(workspace_path)
                            files.append(str(relative_path))
                        except ValueError:
                            # File is outside workspace
                            continue
            
            return sorted(files)[:20]  # Limit to 20 files
            
        except Exception:
            return []

    async def run(self, user_id: str = "default") -> str:
        """Execute agent loop until task is complete or max steps reached."""
        # Start new session if not already started
        if not self.current_session and self.session_manager:
            await self.start_session(user_id)

        # Start new run, initialize log file
        self.logger.start_new_run()
        print(f"{Colors.DIM}[LOG] Log file: {self.logger.get_log_file_path()}{Colors.RESET}")

        step = 0

        while step < self.max_steps:
            # Update session activity
            await self.update_session_activity()

            # Check and summarize message history to prevent context overflow
            await self._summarize_messages()
            
            # Monitor context overflow status
            if step > 0 and step % 5 == 0:  # Every 5 steps
                context_status = self.context_manager.get_status_report()
                if context_status["needs_optimization"]:
                    print(f"\n{Colors.BRIGHT_YELLOW}[CONTEXT] Optimization needed - usage: {context_status['usage_percentage']:.1f}%{Colors.RESET}")
                elif context_status['usage_percentage'] > 40:  # Monitor higher usage
                    print(f"{Colors.DIM}[CONTEXT] Context usage: {context_status['usage_percentage']:.1f}% ({context_status['current_tokens']:,} tokens){Colors.RESET}")

            # Check if the current task might benefit from orchestration
            current_task = self._extract_current_task()
            if step == 0 and current_task and self._is_complex_task(current_task, self._extract_task_context()):
                print(f"\n{Colors.BRIGHT_CYAN}[ORCHESTRATION] Complex task detected, switching to orchestrated execution{Colors.RESET}")
                return await self._execute_orchestrated_task(current_task)

            # Step header with proper width calculation
            BOX_WIDTH = 20  # Reduced from 58 for cleaner output
            step_text = f"{Colors.BOLD}{Colors.BRIGHT_CYAN}[EXECUTION] Step {step + 1}/{self.max_steps}{Colors.RESET}"
            step_display_width = calculate_display_width(step_text)
            padding = max(0, BOX_WIDTH - 1 - step_display_width)  # -1 for leading space

            print(f"\n{Colors.DIM}─{'─' * BOX_WIDTH}─{Colors.RESET}")
            print(f"{Colors.DIM}│{Colors.RESET} {step_text}{' ' * padding}{Colors.DIM}│{Colors.RESET}")
            print(f"{Colors.DIM}─{'─' * BOX_WIDTH}─{Colors.RESET}")

            # Check token budget before LLM call
            context_messages = [msg.__dict__ for msg in self.messages]
            if not self.context_manager.check_token_budget_before_llm(context_messages):
                print(f"\n{Colors.BRIGHT_YELLOW}[CONTEXT] Token budget approaching limit - optimization recommended{Colors.RESET}")
                
                # Get optimization recommendations
                recommendations = self.context_manager.get_optimization_recommendations()
                for rec in recommendations:
                    print(f"{Colors.DIM}   {ICON_INFO} {rec}{Colors.RESET}")

            # Get tool list for LLM call
            tool_list = list(self.tools.values())

            # Log LLM request and call LLM with Tool objects directly
            self.logger.log_request(messages=self.messages, tools=tool_list)

            try:
                # Use error recovery for LLM calls if available
                if self.error_recovery:
                    response_result = await self.error_recovery.execute_with_recovery(
                        operation="llm_generation",
                        func=lambda: self.llm.generate(messages=self.messages, tools=tool_list),
                        context={'step': step, 'max_steps': self.max_steps}
                    )
                    
                    # Handle both string responses (from fallbacks) and LLMResponse objects
                    if isinstance(response_result, str):
                        from .schema import LLMResponse
                        response = LLMResponse(
                            content=response_result,
                            thinking=None,
                            tool_calls=None,
                            finish_reason="fallback",
                        )
                    else:
                        response = response_result
                else:
                    response = await self.llm.generate(messages=self.messages, tools=tool_list)
                    
            except Exception as e:
                # Enhanced error handling with session tracking
                error_context = {
                    'error': str(e),
                    'component': 'llm_generation',
                    'operation': f'step_{step}',
                    'step': step,
                    'max_steps': self.max_steps
                }
                
                await self.add_session_error(error_context)
                
                # Check if it's a retry exhausted error
                from .retry import RetryExhaustedError

                if isinstance(e, RetryExhaustedError):
                    error_msg = f"LLM call failed after {e.attempts} retries\nLast error: {str(e.last_exception)}"
                    print(f"\n{Colors.BRIGHT_RED}{ICON_ERROR} Retry failed:{Colors.RESET} {error_msg}")
                else:
                    error_msg = f"LLM call failed: {str(e)}"
                    print(f"\n{Colors.BRIGHT_RED}{ICON_ERROR} Error:{Colors.RESET} {error_msg}")
                
                # Create a proper error response instead of returning a string
                from .schema import LLMResponse
                response = LLMResponse(
                    content=error_msg,
                    thinking=None,
                    tool_calls=None,
                    finish_reason="error",
                )

            # Log LLM response
            self.logger.log_response(
                content=response.content,
                thinking=response.thinking,
                tool_calls=response.tool_calls,
                finish_reason=response.finish_reason,
            )

            # Add assistant message
            assistant_msg = Message(
                role="assistant",
                content=response.content,
                thinking=response.thinking,
                tool_calls=response.tool_calls,
            )
            self.messages.append(assistant_msg)

            # Print thinking if present
            if response.thinking:
                print(f"\n{Colors.BOLD}{Colors.MAGENTA}[THINKING] Thinking:{Colors.RESET}")
                print(f"{Colors.DIM}{response.thinking}{Colors.RESET}")

            # Print assistant response
            if response.content:
                print(f"\n{Colors.BOLD}{Colors.BRIGHT_BLUE}[ASSISTANT] Assistant:{Colors.RESET}")
                print(f"{response.content}")

            # Check if task is complete (no tool calls) - Apply QA validation before declaring completion
            if not response.tool_calls:
                # Validate task completion before declaring it done
                validation_result = await self._validate_task_completion(response)
                
                # Handle validation results
                if validation_result:
                    if isinstance(validation_result, dict):
                        honesty_score = validation_result.get('honesty_score', 0)
                        feedback = validation_result.get('feedback', '')
                        
                        if honesty_score >= 80:
                            # High honesty score - genuine completion
                            print(f"\n{Colors.BRIGHT_GREEN}[SUCCESS] TASK VALIDATION PASSED{Colors.RESET}")
                            if feedback:
                                print(f"{Colors.DIM}[FEEDBACK] {feedback}{Colors.RESET}")
                            return response.content if hasattr(response, 'content') else str(response)
                        else:
                            # Low honesty score - needs improvement
                            print(f"\n{Colors.BRIGHT_YELLOW}[QUALITY] QUALITY ASSESSMENT REQUIRED{Colors.RESET}")
                            print(f"{Colors.DIM}[SCORE] Honesty Score: {honesty_score}/100{Colors.RESET}")
                            
                            if validation_result.get('feedback'):
                                print(f"\n{Colors.DIM}[TOOL] Feedback:{Colors.RESET}")
                                feedback_text = validation_result['feedback']
                                if isinstance(feedback_text, str):
                                    for issue in feedback_text.split('\n'):
                                        if issue.strip():
                                            print(f"   {Colors.DIM}{ICON_INFO} {issue}{Colors.RESET}")
                                else:
                                    print(f"   {Colors.DIM}{ICON_INFO} {feedback_text}{Colors.RESET}")
                            
                            if validation_result.get('deception_patterns'):
                                print(f"\n{Colors.BRIGHT_RED}[ISSUE]  DETECTED ISSUES:{Colors.RESET}")
                                deception_patterns = validation_result['deception_patterns']
                                if isinstance(deception_patterns, list):
                                    for pattern in deception_patterns:
                                        if pattern:
                                            print(f"   {Colors.BRIGHT_RED}{ICON_ERROR} {pattern}{Colors.RESET}")
                            
                            # Continue iteration to address issues
                            assistant_msg.content += f"\n\n**Quality Assessment**: {validation_result.get('feedback', 'Please review your work and ensure all requirements are fully met.')}"
                            self.messages[-1] = assistant_msg
                            continue
                    else:
                        # Handle non-dict validation result
                        print(f"{Colors.DIM}[DEBUG] Validation returned non-dict result, treating as passed{Colors.RESET}")
                        # Handle both string responses and LLMResponse objects
                        if hasattr(response, 'content'):
                            return response.content if hasattr(response, 'content') else str(response)
                        else:
                            # response is already a string
                            return str(response)
                else:
                    # No validation system available - proceed with original behavior
                    print(f"\n{Colors.DIM}[ISSUE]  Validation system not available - proceeding{Colors.RESET}")
                    return response.content if hasattr(response, 'content') else str(response)

            # Execute tool calls with enhanced error recovery
            for tool_call in response.tool_calls:
                tool_call_id = tool_call.id
                function_name = tool_call.function.name
                arguments = tool_call.function.arguments

                # Tool call header
                print(f"\n{Colors.BRIGHT_YELLOW}[TOOL] Tool Call:{Colors.RESET} {Colors.BOLD}{Colors.CYAN}{function_name}{Colors.RESET}")

                # Arguments (formatted display)
                print(f"{Colors.DIM}   Arguments:{Colors.RESET}")
                # Truncate each argument value to avoid overly long output
                truncated_args = {}
                for key, value in arguments.items():
                    value_str = str(value)
                    if len(value_str) > 200:
                        truncated_args[key] = value_str[:200] + "..."
                    else:
                        truncated_args[key] = value
                args_json = json.dumps(truncated_args, indent=2, ensure_ascii=False)
                for line in args_json.split("\n"):
                    print(f"   {Colors.DIM}{line}{Colors.RESET}")

                # Execute tool with error recovery
                try:
                    if function_name not in self.tools:
                        result = ToolResult(
                            success=False,
                            content="",
                            error=f"Unknown tool: {function_name}",
                        )
                    else:
                        tool = self.tools[function_name]
                        
                        # Use error recovery for tool execution
                        if self.error_recovery:
                            # Create a proper wrapper function that works with error recovery system
                            async def execute_tool_with_recovery(*args, **kwargs):
                                # The error recovery system will pass arguments, but we want to use our captured ones
                                return await tool.execute(**arguments)
                            
                            result = await self.error_recovery.execute_with_recovery(
                                operation=f"tool_{function_name}",
                                func=execute_tool_with_recovery,
                                context={'tool_name': function_name, 'arguments': arguments}
                            )
                        else:
                            result = await tool.execute(**arguments)
                            
                except Exception as e:
                    # Enhanced error handling for tool execution
                    error_context = {
                        'error': str(e),
                        'component': 'tool_execution',
                        'operation': function_name,
                        'arguments': arguments
                    }
                    
                    await self.add_session_error(error_context)
                    
                    # Convert exception to failed ToolResult
                    import traceback

                    error_detail = f"{type(e).__name__}: {str(e)}"
                    error_trace = traceback.format_exc()
                    result = ToolResult(
                        success=False,
                        content="",
                        error=f"Tool execution failed: {error_detail}\n\nTraceback:\n{error_trace}",
                    )

                # Log tool execution result
                self.logger.log_tool_result(
                    tool_name=function_name,
                    arguments=arguments,
                    result_success=result.success,
                    result_content=result.content if result.success else None,
                    result_error=result.error if not result.success else None,
                )

                # Print result
                if result.success:
                    result_text = result.content
                    if len(result_text) > 300:
                        result_text = result_text[:300] + f"{Colors.DIM}...{Colors.RESET}"
                    print(f"{Colors.BRIGHT_GREEN}[SUCCESS] Result:{Colors.RESET} {result_text}")
                else:
                    print(f"{Colors.BRIGHT_RED}{ICON_ERROR} Error:{Colors.RESET} {Colors.RED}{result.error}{Colors.RESET}")

                # Add tool result message
                tool_msg = Message(
                    role="tool",
                    content=result.content if result.success else f"Error: {result.error}",
                    tool_call_id=tool_call_id,
                    name=function_name,
                )
                self.messages.append(tool_msg)

            step += 1

        # Max steps reached
        error_msg = f"Task couldn't be completed after {self.max_steps} steps."
        print(f"\n{Colors.BRIGHT_YELLOW}[ISSUE]  {error_msg}{Colors.RESET}")
        return error_msg

    async def _execute_tool_safely(self, tool: Tool, **kwargs) -> ToolResult:
        """Safely execute a tool with exception handling"""
        return await tool.execute(**kwargs)

    async def _call_llm_with_tools(self, tools: List[Tool]) -> Any:
        """Call LLM with tools (for error recovery wrapper)"""
        return await self.llm.generate(messages=self.messages, tools=tools)

    async def _execute_orchestrated_task(self, task_description: str) -> str:
        """Execute task using orchestration system"""
        try:
            # Get task context
            context = self._extract_task_context()
            
            # Execute using orchestrator
            result = await self.execute_complex_task(task_description, context)
            
            # Extract content from result
            if hasattr(result, 'result') and isinstance(result.result, dict):
                if 'result' in result.result:
                    return result.result['result']
                else:
                    # Format the results nicely
                    output_parts = []
                    for key, value in result.result.items():
                        if key.startswith('subtask_'):
                            subtask_id = key.replace('subtask_', '')
                            if isinstance(value, dict) and 'result' in value:
                                output_parts.append(f"**{subtask_id}:** {value['result']}")
                            else:
                                output_parts.append(f"**{subtask_id}:** {value}")
                    
                    if output_parts:
                        return "\n\n".join(output_parts)
                    else:
                        return str(result.result)
            else:
                return str(result.result if hasattr(result, 'result') else result)
                
        except Exception as e:
            logger.error(f"Orchestrated task execution failed: {e}")
            error_msg = f"Orchestrated task execution failed: {e}"
            print(f"\n{Colors.BRIGHT_RED}[ERROR] {error_msg}{Colors.RESET}")
            return error_msg

    def _extract_current_task(self) -> Optional[str]:
        """Extract the current task description from messages"""
        for msg in reversed(self.messages):
            if msg.role == "user" and not msg.content.startswith("[Assistant Execution Summary]"):
                return msg.content
        return None

    def _extract_task_context(self) -> Dict[str, Any]:
        """Extract context information for task execution"""
        context = {
            'message_count': len(self.messages),
            'current_tokens': self._estimate_tokens(),
            'tools_available': list(self.tools.keys()),
            'session_id': self.current_session.session_id if self.current_session else None
        }
        
        # Extract any specific context from recent messages
        for msg in reversed(self.messages[-3:]):  # Check last 3 messages
            if msg.role == "user":
                content = msg.content
                if "project" in content.lower():
                    context['project_context'] = content[:200]
                if "requirements" in content.lower():
                    context['requirements_context'] = content[:200]
        
        return context

    async def start_session(self, user_id: str = "default", metadata: Dict[str, Any] = None) -> str:
        """Start a new session for this agent"""
        if not self.session_manager:
            logger.warning("Session manager not available")
            return None

        try:
            session = await self.session_manager.create_session(user_id, metadata)
            self.current_session = session
            
            # Update activity with current context size
            current_tokens = self._estimate_tokens()
            await self.session_manager.update_activity(session.session_id, current_tokens)
            
            print(f"{Colors.BRIGHT_GREEN}[SESSION] Started session: {session.session_id[:8]}...{Colors.RESET}")
            return session.session_id
            
        except Exception as e:
            logger.error(f"Failed to start session: {e}")
            return None

    async def update_session_activity(self):
        """Update current session activity"""
        if not self.session_manager or not self.current_session:
            return

        try:
            current_tokens = self._estimate_tokens()
            await self.session_manager.update_activity(
                self.current_session.session_id, 
                current_tokens
            )
        except Exception as e:
            logger.warning(f"Failed to update session activity: {e}")

    async def add_session_error(self, error_info: Dict[str, Any]):
        """Add error to current session"""
        if not self.session_manager or not self.current_session:
            return

        try:
            await self.session_manager.add_session_error(
                self.current_session.session_id, 
                error_info
            )
        except Exception as e:
            logger.warning(f"Failed to add session error: {e}")

    def _is_complex_task(self, task_description: str, context: Dict[str, Any] = None) -> bool:
        """Determine if a task requires orchestration"""
        if not self.task_orchestrator:
            return False

        complexity_indicators = [
            len(task_description) > 500,
            'complex' in task_description.lower(),
            'multiple' in task_description.lower(),
            'analysis' in task_description.lower() and 'data' in task_description.lower(),
            'comprehensive' in task_description.lower(),
            'integration' in task_description.lower(),
            'development' in task_description.lower() and ('system' in task_description.lower() or 'application' in task_description.lower())
        ]

        # Also check context size
        context_tokens = self._estimate_tokens()

        # Consider using orchestration for complex tasks
        score = sum(complexity_indicators)
        return score >= 2 or context_tokens > 50000

    async def execute_task_with_context(self, task: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute a task with provided context (used by task orchestrator)"""
        
        # Add task-specific context to messages
        task_context_msg = Message(
            role="system", 
            content=f"Task Context: {task.get('description', 'Unknown task')}"
        )
        self.messages.append(task_context_msg)

        # Add any additional context
        if 'focus' in context:
            focus_msg = Message(
                role="system",
                content=f"Execution Focus: {context['focus']}"
            )
            self.messages.append(focus_msg)

        try:
            # Execute task using existing agent logic but with enhanced error recovery
            if self.error_recovery:
                return await self.error_recovery.execute_with_recovery(
                    operation="task_execution",
                    func=lambda task=task, context=context: self._execute_single_task(task, context),
                    context={'task': task, 'context': context}
                )
            else:
                return await self._execute_single_task(task, context)
                
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            if self.session_manager and self.current_session:
                await self.add_session_error({
                    'error': str(e),
                    'component': 'task_execution',
                    'operation': task.get('id', 'unknown')
                })
            raise

    async def _execute_single_task(self, task: Dict[str, Any], context: Dict[str, Any]) -> Any:
        """Execute a single task (used by orchestrator)"""
        # For now, execute as a simple LLM call with the task context
        task_prompt = f"""
        Execute the following task:
        
        {task.get('description', 'No description provided')}
        
        Context: {context}
        
        Please provide a comprehensive and detailed response to complete this task.
        """
        
        task_message = Message(role="user", content=task_prompt)
        self.messages.append(task_message)

        try:
            response = await self.llm.generate(messages=self.messages, tools=list(self.tools.values()))
            return response.content
        except Exception as e:
            logger.error(f"Single task execution failed: {e}")
            raise

    async def execute_complex_task(self, task_description: str, context: Dict[str, Any] = None) -> Any:
        """Execute a complex task using task orchestration"""
        if not self.task_orchestrator:
            logger.warning("Task orchestrator not available, falling back to direct execution")
            return await self._execute_direct_task(task_description, context)

        try:
            print(f"{Colors.BRIGHT_CYAN}[ORCHESTRATION] Complex task detected, using task orchestration{Colors.RESET}")
            
            # Update session activity
            await self.update_session_activity()
            
            # Execute using task orchestrator
            result = await self.task_orchestrator.execute_complex_task(task_description, context)
            
            # Update session activity with result size
            if self.session_manager and self.current_session:
                await self.session_manager.update_activity(
                    self.current_session.session_id,
                    len(str(result.result)) // 4  # Rough token estimate
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Complex task execution failed: {e}")
            if self.session_manager and self.current_session:
                await self.add_session_error({
                    'error': str(e),
                    'component': 'task_orchestration',
                    'operation': 'complex_task_execution'
                })
            raise

    async def _execute_direct_task(self, task_description: str, context: Dict[str, Any] = None) -> Any:
        """Execute a task directly without orchestration"""
        
        # Add user message
        user_message = Message(role="user", content=task_description)
        self.messages.append(user_message)

        try:
            # Simple direct execution with error recovery
            if self.error_recovery:
                return await self.error_recovery.execute_with_recovery(
                    operation="direct_task_execution",
                    func=lambda: self._call_llm_direct(),
                    context={'task': task_description, 'context': context}
                )
            else:
                return await self._call_llm_direct()
                
        except Exception as e:
            logger.error(f"Direct task execution failed: {e}")
            if self.session_manager and self.current_session:
                await self.add_session_error({
                    'error': str(e),
                    'component': 'direct_execution',
                    'operation': 'task_execution'
                })
            raise

    async def _call_llm_direct(self) -> Any:
        """Direct LLM call for simple tasks"""
        try:
            tool_list = list(self.tools.values())
            response = await self.llm.generate(messages=self.messages, tools=tool_list)
            return response.content
        except Exception as e:
            logger.error(f"Direct LLM call failed: {e}")
            raise

    def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the enhanced agent"""
        status = {
            'basic_info': {
                'max_steps': self.max_steps,
                'token_limit': self.token_limit,
                'current_tokens': self._estimate_tokens(),
                'messages_count': len(self.messages),
                'tools_count': len(self.tools)
            },
            'enhanced_components': {
                'task_orchestrator': self.task_orchestrator is not None,
                'session_manager': self.session_manager is not None,
                'error_recovery': self.error_recovery is not None,
                'current_session': self.current_session.session_id if self.current_session else None
            }
        }

        # Add detailed status for each component
        if self.task_orchestrator:
            status['task_orchestrator'] = self.task_orchestrator.get_orchestrator_status()

        if self.session_manager and self.current_session:
            status['session_info'] = {
                'session_id': self.current_session.session_id,
                'state': self.current_session.state.value,
                'context_size': self.current_session.context_size,
                'created_at': self.current_session.created_at,
                'last_activity': self.current_session.last_activity
            }
            try:
                status['session_statistics'] = self.session_manager.get_session_statistics()
            except:
                status['session_statistics'] = {'error': 'Failed to get session statistics'}

        if self.error_recovery:
            status['error_recovery'] = self.error_recovery.get_recovery_status()

        return status

    def get_history(self) -> list[Message]:
        """Get message history."""
        return self.messages.copy()
        """Get message history."""
        return self.messages.copy()