"""Core Agent implementation."""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

import tiktoken

from .llm import LLMClient
from .logger import AgentLogger
from .schema import Message
from .tools.base import Tool, ToolResult
from .utils import calculate_display_width
from .core.context_overflow_prevention import get_context_manager


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
    """Single agent with basic tools and MCP support."""

    def __init__(
        self,
        llm_client: LLMClient,
        system_prompt: str,
        tools: list[Tool],
        max_steps: int = 50,
        workspace_dir: str = "./workspace",
        token_limit: int = 200000,  # Summary triggered when tokens exceed this value (updated for 200K context)
    ):
        self.llm = llm_client
        self.tools = {tool.name: tool for tool in tools}
        self.max_steps = max_steps
        self.token_limit = token_limit
        self.workspace_dir = Path(workspace_dir)

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
        self.context_manager = get_context_manager()

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

    async def run(self) -> str:
        """Execute agent loop until task is complete or max steps reached."""
        # Start new run, initialize log file
        self.logger.start_new_run()
        print(f"{Colors.DIM}[LOG] Log file: {self.logger.get_log_file_path()}{Colors.RESET}")

        step = 0

        while step < self.max_steps:
            # Check and summarize message history to prevent context overflow
            await self._summarize_messages()
            
            # Monitor context overflow status
            if step > 0 and step % 5 == 0:  # Every 5 steps
                context_status = self.context_manager.get_status_report()
                if context_status["needs_optimization"]:
                    print(f"\n{Colors.BRIGHT_YELLOW}[CONTEXT] Optimization needed - usage: {context_status['usage_percentage']:.1f}%{Colors.RESET}")
                elif context_status['usage_percentage'] > 40:  # Monitor higher usage
                    print(f"{Colors.DIM}[CONTEXT] Context usage: {context_status['usage_percentage']:.1f}% ({context_status['current_tokens']:,} tokens){Colors.RESET}")

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
                response = await self.llm.generate(messages=self.messages, tools=tool_list)
            except Exception as e:
                # Check if it's a retry exhausted error
                from .retry import RetryExhaustedError

                if isinstance(e, RetryExhaustedError):
                    error_msg = f"LLM call failed after {e.attempts} retries\nLast error: {str(e.last_exception)}"
                    print(f"\n{Colors.BRIGHT_RED}{ICON_ERROR} Retry failed:{Colors.RESET} {error_msg}")
                else:
                    error_msg = f"LLM call failed: {str(e)}"
                    print(f"\n{Colors.BRIGHT_RED}{ICON_ERROR} Error:{Colors.RESET} {error_msg}")
                return error_msg

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
                
                # Handle both dict and string results from validation
                if validation_result:
                    # Check if validation_result is a dict (expected format)
                    if isinstance(validation_result, dict):
                        honesty_score = validation_result.get('honesty_score', 0)
                    else:
                        # Handle case where validation_result is a string
                        print(f"{Colors.DIM}[DEBUG] Validation returned string, treating as passed{Colors.RESET}")
                        honesty_score = 100  # Default to high score for string results
                    
                    if honesty_score >= 80:
                        # High honesty score - genuine completion
                        print(f"\n{Colors.BRIGHT_GREEN}[SUCCESS] TASK VALIDATION PASSED{Colors.RESET}")
                    if isinstance(validation_result, dict) and validation_result.get('feedback'):
                        print(f"{Colors.DIM}[FEEDBACK] {validation_result['feedback']}{Colors.RESET}")
                    return response.content
                elif validation_result:
                    # Validation failed or low honesty score
                    print(f"\n{Colors.BRIGHT_YELLOW}[QUALITY] QUALITY ASSESSMENT REQUIRED{Colors.RESET}")
                    
                    if isinstance(validation_result, dict):
                        honesty_score = validation_result.get('honesty_score', 0)
                        print(f"{Colors.DIM}[SCORE] Honesty Score: {honesty_score}/100{Colors.RESET}")
                        
                        if validation_result.get('feedback'):
                            print(f"\n{Colors.DIM}[TOOL] Feedback:{Colors.RESET}")
                            for issue in validation_result['feedback'].split('\n'):
                                if issue.strip():
                                    print(f"   {Colors.DIM}{ICON_INFO} {issue}{Colors.RESET}")
                        
                        if validation_result.get('deception_patterns'):
                            print(f"\n{Colors.BRIGHT_RED}[ISSUE]  DETECTED ISSUES:{Colors.RESET}")
                            for pattern in validation_result['deception_patterns']:
                                print(f"   {Colors.BRIGHT_RED}{ICON_ERROR} {pattern}{Colors.RESET}")
                        
                        # Continue iteration to address issues
                        assistant_msg.content += f"\n\n**Quality Assessment**: {validation_result.get('feedback', 'Please review your work and ensure all requirements are fully met.')}"
                    else:
                        # Handle string result case
                        print(f"{Colors.DIM}[SCORE] Validation score: Unable to parse{Colors.RESET}")
                        assistant_msg.content += f"\n\n**Quality Assessment**: {validation_result}"
                    continue
                    self.messages[-1] = assistant_msg  # Update the message
                    continue  # Continue to next step
                else:
                    # No validation system available - proceed with original behavior
                    print(f"\n{Colors.DIM}[ISSUE]  Validation system not available - proceeding{Colors.RESET}")
                    return response.content

            # Execute tool calls
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

                # Execute tool
                if function_name not in self.tools:
                    result = ToolResult(
                        success=False,
                        content="",
                        error=f"Unknown tool: {function_name}",
                    )
                else:
                    try:
                        tool = self.tools[function_name]
                        result = await tool.execute(**arguments)
                    except Exception as e:
                        # Catch all exceptions during tool execution, convert to failed ToolResult
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

    def get_history(self) -> list[Message]:
        """Get message history."""
        return self.messages.copy()