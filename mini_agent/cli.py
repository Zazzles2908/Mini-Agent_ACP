"""
Mini Agent - Interactive Runtime Example

Usage:
    mini-agent [--workspace DIR]

Examples:
    mini-agent                              # Use current directory as workspace
    mini-agent --workspace /path/to/dir     # Use specific workspace directory
"""

import argparse
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

from mini_agent import LLMClient
from mini_agent.agent import Agent
from mini_agent.config import get_config
from mini_agent.config.__init__ import Config
from mini_agent.schema import LLMProvider
from mini_agent.tools.base import Tool
from mini_agent.tools.bash_tool import BashKillTool, BashOutputTool, BashTool
from mini_agent.tools.file_tools import EditTool, ReadTool, WriteTool
from mini_agent.tools.mcp_loader import cleanup_mcp_connections, load_mcp_tools_async
from mini_agent.tools.note_tool import SessionNoteTool
from mini_agent.tools.skill_tool import create_skill_tools
from mini_agent.utils import calculate_display_width


# ANSI color codes
class Colors:
    """Terminal color definitions"""

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def print_banner():
    """Print welcome banner"""
    banner = """
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                      🏭 Mini-Agent                             │
│                    Interactive Agent                           │
│                                                                 │
│  ✨ Powered by MiniMax-M2                                       │
│  🔧 File operations, shell commands, web search, skills         │
│  🚀 Ready to help you accomplish your goals                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
"""
    print(f"{Colors.GREEN}{banner}{Colors.RESET}")


def print_help():
    """Print help information"""
    help_text = """
🤖 Available Commands:
  /help    - Show this help message
  /clear   - Clear the screen
  /history - Show message history
  /stats   - Show session statistics
  /exit    - Exit the agent

💡 Tips:
  • Describe what you want to accomplish, I'll break it down into steps
  • Use tools like file operations, web search, and code execution as needed
  • I'll remember our conversation context
  • Use /stats to see your session progress
"""
    print(f"{Colors.CYAN}{help_text}{Colors.RESET}")


def print_session_info(agent: Agent, workspace_dir: Path, model: str):
    """Print session information"""
    def print_info_line(text: str):
        """Print an info line with consistent formatting"""
        print(f"  {Colors.BRIGHT_CYAN}{text}{Colors.RESET}")

    print_info_line("Session started")
    print_info_line(f"Model: {model}")
    print_info_line(f"Workspace: {workspace_dir}")
    print_info_line(f"Tools: {len(agent.tools)} available")
    print_info_line(f"Max steps: {agent.max_steps}")
    print()
    
    print(f"{Colors.BRIGHT_YELLOW}Available Tools:{Colors.RESET}")
    # Group tools by category
    file_tools = [t for t in agent.tools.values() if "read" in t.name.lower() or "write" in t.name.lower() or "edit" in t.name.lower()]
    bash_tools = [t for t in agent.tools.values() if "bash" in t.name.lower()]
    skill_tools = [t for t in agent.tools.values() if "skill" in t.name.lower()]
    other_tools = [t for t in agent.tools.values() if t not in file_tools + bash_tools + skill_tools]

    if file_tools:
        print(f"  {Colors.GREEN}📁 File Operations:{Colors.RESET}")
        for tool in file_tools:
            print(f"    • {tool.name}: {tool.description}")
    
    if bash_tools:
        print(f"  {Colors.GREEN}💻 Shell Commands:{Colors.RESET}")
        for tool in bash_tools:
            print(f"    • {tool.name}: {tool.description}")
    
    if skill_tools:
        print(f"  {Colors.GREEN}🔧 Skills:{Colors.RESET}")
        for tool in skill_tools:
            print(f"    • {tool.name}: {tool.description}")
    
    if other_tools:
        print(f"  {Colors.GREEN}⚙️  Other Tools:{Colors.RESET}")
        for tool in other_tools:
            print(f"    • {tool.name}: {tool.description}")
    
    print()


def print_stats(agent: Agent, session_start: datetime):
    """Print session statistics"""
    duration = datetime.now() - session_start
    hours, remainder = divmod(int(duration.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    print(f"\n{Colors.BRIGHT_CYAN}📊 Session Statistics:{Colors.RESET}")
    print(f"  Duration: {hours}h {minutes}m {seconds}s")
    print(f"  Messages: {len(agent.messages)} total")
    print(f"  Steps used: {agent._current_step}/{agent.max_steps} max")
    print(f"  Tools available: {len(agent.tools)}")
    print()


async def initialize_base_tools(config: Config):
    """Initialize base tools (independent of workspace)

    These tools are loaded from package configuration and don't depend on workspace.
    Note: File tools are now workspace-dependent and initialized in add_workspace_tools()

    Args:
        config: Configuration object

    Returns:
        Tuple of (list of tools, skill loader if skills enabled)
    """

    tools = []
    skill_loader = None

    # 1. Bash tool and Bash Output tool
    if config.tools.get("enable_bash", True):
        bash_tool = BashTool()
        tools.append(bash_tool)
        print(f"{Colors.GREEN}✅ Loaded Bash tool{Colors.RESET}")

        bash_output_tool = BashOutputTool()
        tools.append(bash_output_tool)
        print(f"{Colors.GREEN}✅ Loaded Bash Output tool{Colors.RESET}")

        bash_kill_tool = BashKillTool()
        tools.append(bash_kill_tool)
        print(f"{Colors.GREEN}✅ Loaded Bash Kill tool{Colors.RESET}")

    # 3. MiniMax-M2 Skills (loaded from package directory)
    if config.tools.get("enable_skills", True):
        print(f"{Colors.BRIGHT_CYAN}Loading MiniMax-M2 Skills...{Colors.RESET}")
        try:
            # Resolve skills directory with priority search
            skills_dir = config.tools.get("skills_dir", "./skills")
            if not Path(skills_dir).is_absolute():
                # Search in priority order:
                # 1. Current directory (dev mode: ./skills or ./mini_agent/skills)
                # 2. Package directory (installed: site-packages/mini_agent/skills)
                search_paths = [
                    Path(skills_dir),  # ./skills for backward compatibility
                    Path("mini_agent") / skills_dir,  # ./mini_agent/skills
                    Config.get_package_dir() / skills_dir,  # site-packages/mini_agent/skills
                ]

                # Find first existing path
                for path in search_paths:
                    if path.exists():
                        skills_dir = str(path.resolve())
                        break

            skill_tools, skill_loader = create_skill_tools(skills_dir)
            if skill_tools:
                tools.extend(skill_tools)
                print(f"{Colors.GREEN}✅ Loaded Skill tool (get_skill){Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}⚠️  No available Skills found{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Failed to load Skills: {e}{Colors.RESET}")

    # 4. MCP Tools
    if config.tools.get("enable_mcp", True):
        print(f"{Colors.BRIGHT_CYAN}Loading MCP tools...{Colors.RESET}")
        try:
            # Use priority search for mcp.json
            mcp_config_path = get_config().find_config_file(config.tools.get("mcp_config_path", "mcp.json"))
            if mcp_config_path:
                mcp_tools = await load_mcp_tools_async(str(mcp_config_path))
                if mcp_tools:
                    tools.extend(mcp_tools)
                    print(f"{Colors.GREEN}✅ Loaded {len(mcp_tools)} MCP tools (from: {mcp_config_path}){Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}⚠️  No available MCP tools found{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}⚠️  MCP config file not found: {config.tools.get('mcp_config_path', 'mcp.json')}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Failed to load MCP tools: {e}{Colors.RESET}")

    # 5. Z.AI Web Tools (MCP-First Hybrid)
    zai_enabled = config.tools.get("enable_zai_search", False) or config.tools.get("enable_zai_web_tools", False)
    if zai_enabled:
        print(f"{Colors.BRIGHT_CYAN}Loading Z.AI Web Tools...{Colors.RESET}")
        try:
            # Use HTTP-based Z.AI tools (replacing the old unified client)
            from mini_agent.tools.zai_web_tool import ZAIWebTool
            zai_tool = ZAIWebTool()
            tools.append(zai_tool)
            print(f"{Colors.GREEN}✅ Loaded Z.AI Web Tools (HTTP-based){Colors.RESET}")
        except Exception as e:
            print(f"{Colors.YELLOW}⚠️  Failed to load Z.AI Web Tools: {e}{Colors.RESET}")

    # 6. Session Note Tool (always load for memory)
    tools.append(SessionNoteTool())
    print(f"{Colors.GREEN}✅ Loaded Session Note tool{Colors.RESET}")

    return tools, skill_loader


def add_workspace_tools(tools: List[Tool], config: Config, workspace_dir: Path):
    """Add workspace-dependent tools

    These tools need to know the workspace directory.

    Args:
        tools: Existing tools list to add to
        config: Configuration object
        workspace_dir: Workspace directory path
    """
    # Ensure workspace directory exists
    workspace_dir.mkdir(parents=True, exist_ok=True)

    # File tools - need workspace to resolve relative paths
    if config.tools.get("enable_file_tools", True):
        tools.extend(
            [
                ReadTool(workspace_dir=str(workspace_dir)),
                WriteTool(workspace_dir=str(workspace_dir)),
                EditTool(workspace_dir=str(workspace_dir)),
            ]
        )
        print(f"{Colors.GREEN}✅ Loaded file operation tools (workspace: {workspace_dir}){Colors.RESET}")

    # Session note tool - needs workspace to store memory file
    if config.tools.get("enable_note", True):
        tools.append(SessionNoteTool(memory_file=str(workspace_dir / ".agent_memory.json")))
        print(f"{Colors.GREEN}✅ Loaded session note tool{Colors.RESET}")


async def run_agent(workspace_dir: Path):
    """Run interactive Agent

    Args:
        workspace_dir: Workspace directory path
    """
    session_start = datetime.now()

    # 1. Load configuration from package directory
    config_path = get_config().get_default_config_path()

    if not config_path.exists():
        print(f"{Colors.RED}❌ Configuration file not found{Colors.RESET}")
        print()
        print(f"{Colors.BRIGHT_CYAN}📦 Configuration Search Path:{Colors.RESET}")
        print(f"  {Colors.DIM}1) mini_agent/config/config.yaml{Colors.RESET} (development)")
        print(f"  {Colors.DIM}2) ~/.mini-agent/config/config.yaml{Colors.RESET} (user)")
        print(f"  {Colors.DIM}3) <package>/config/config.yaml{Colors.RESET} (installed)")
        print()
        print(f"{Colors.BRIGHT_YELLOW}🚀 Quick Setup (Recommended):{Colors.RESET}")
        print(f"  {Colors.BRIGHT_GREEN}curl -fsSL https://raw.githubusercontent.com/MiniMax-AI/Mini-Agent/main/scripts/setup-config.sh | bash{Colors.RESET}")
        print()
        print(f"{Colors.DIM}  This will automatically:{Colors.RESET}")
        print(f"{Colors.DIM}    • Create ~/.mini-agent/config/{Colors.RESET}")
        print(f"{Colors.DIM}    • Download configuration files{Colors.RESET}")
        print(f"{Colors.DIM}    • Guide you to add your API Key{Colors.RESET}")
        print()
        print(f"{Colors.BRIGHT_YELLOW}📝 Manual Setup:{Colors.RESET}")
        user_config_dir = Path.home() / ".mini-agent" / "config"
        example_config = get_config().get_package_dir() / "config" / "config-example.yaml"
        print(f"  {Colors.DIM}mkdir -p {user_config_dir}{Colors.RESET}")
        print(f"  {Colors.DIM}cp {example_config} {user_config_dir}/config.yaml{Colors.RESET}")
        print(f"  {Colors.DIM}# Then edit {user_config_dir}/config.yaml to add your API Key{Colors.RESET}")
        print()
        return

    try:
        config = get_config()
    except FileNotFoundError:
        print(f"{Colors.RED}❌ Error: Configuration file not found: {config_path}{Colors.RESET}")
        return
    except ValueError as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        print(f"{Colors.YELLOW}Please check the configuration file format{Colors.RESET}")
        return
    except Exception as e:
        print(f"{Colors.RED}❌ Error: Failed to load configuration file: {e}{Colors.RESET}")
        return

    # 2. Initialize LLM client
    from mini_agent.retry import RetryConfig as RetryConfigBase

    # Convert configuration format
    retry_config = RetryConfigBase(
        enabled=config.retry.get("enabled", True),
        max_retries=config.retry.get("max_retries", 5),
        initial_delay=config.retry.get("initial_delay", 1.0),
        max_delay=config.retry.get("max_delay", 60.0),
        exponential_base=config.retry.get("exponential_base", 2.0),
        retryable_exceptions=(Exception,),
    )

    # Create retry callback function to display retry information in terminal
    def on_retry(exception: Exception, attempt: int):
        """Retry callback function to display retry information"""
        print(f"\n{Colors.BRIGHT_YELLOW}⚠️  LLM call failed (attempt {attempt}): {str(exception)}{Colors.RESET}")
        next_delay = retry_config.calculate_delay(attempt - 1)
        print(f"{Colors.DIM}   Retrying in {next_delay:.1f}s (attempt {attempt + 1})...{Colors.RESET}")

    # Convert provider string to LLMProvider enum (matching reference implementation)
    provider = LLMProvider.ANTHROPIC if config.provider.lower() == "anthropic" else LLMProvider.OPENAI

    llm_client = LLMClient(
        api_key=config.api_key,
        provider=provider,
        api_base=config.api_base,
        model=config.model,
        retry_config=retry_config if config.retry.get("enabled", True) else None,
    )

    # Set retry callback
    if config.retry.get("enabled", True):
        llm_client.retry_callback = on_retry
        print(f"{Colors.GREEN}✅ LLM retry mechanism enabled (max {config.retry.get('max_retries', 5)} retries){Colors.RESET}")

    # 3. Initialize base tools (independent of workspace)
    tools, skill_loader = await initialize_base_tools(config)

    # 4. Add workspace-dependent tools
    add_workspace_tools(tools, config, workspace_dir)

    # 5. Load System Prompt (with priority search)
    system_prompt_path = Config.find_config_file(config.system_prompt_path)
    if system_prompt_path and system_prompt_path.exists():
        system_prompt = system_prompt_path.read_text(encoding="utf-8")
        print(f"{Colors.GREEN}✅ Loaded system prompt (from: {system_prompt_path}){Colors.RESET}")
    else:
        system_prompt = "You are Mini-Agent, an intelligent assistant powered by MiniMax M2 that can help users complete various tasks."
        print(f"{Colors.YELLOW}⚠️  System prompt not found, using default{Colors.RESET}")

    # 6. Inject Skills Metadata into System Prompt (Progressive Disclosure - Level 1)
    if skill_loader:
        skills_metadata = skill_loader.get_skills_metadata_prompt()
        if skills_metadata:
            # Replace placeholder with actual metadata
            system_prompt = system_prompt.replace("{SKILLS_METADATA}", skills_metadata)
            print(f"{Colors.GREEN}✅ Injected {len(skill_loader.loaded_skills)} skills metadata into system prompt{Colors.RESET}")
        else:
            # Remove placeholder if no skills
            system_prompt = system_prompt.replace("{SKILLS_METADATA}", "")
    else:
        # Remove placeholder if skills not enabled
        system_prompt = system_prompt.replace("{SKILLS_METADATA}", "")

    # 7. Create Agent
    agent = Agent(
        llm_client=llm_client,
        system_prompt=system_prompt,
        tools=tools,
        max_steps=config.max_steps,
        workspace_dir=str(workspace_dir),
    )

    # 8. Display welcome information
    print_banner()
    print_session_info(agent, workspace_dir, config.model)

    # 9. Setup prompt_toolkit session
    # Command completer
    command_completer = WordCompleter(
        ["/help", "/clear", "/history", "/stats", "/exit", "/quit", "/q"],
        ignore_case=True,
        sentence=True,
    )

    # Custom style for prompt
    prompt_style = Style.from_dict(
        {
            "prompt": "#00ff00 bold",  # Green and bold
            "separator": "#666666",  # Gray
        }
    )

    # Custom key bindings
    kb = KeyBindings()

    @kb.add("c-u")  # Ctrl+U: Clear current line
    def _(event):
        """Clear the current input line"""
        event.current_buffer.reset()

    @kb.add("c-l")  # Ctrl+L: Clear screen (optional bonus)
    def _(event):
        """Clear the screen"""
        event.app.renderer.clear()

    @kb.add("c-j")  # Ctrl+J (对应 Ctrl+Enter)
    def _(event):
        """Insert a newline"""
        event.current_buffer.insert_text("\n")

    # Create prompt session with history and auto-suggest
    session = PromptSession(
        history=InMemoryHistory(),
        auto_suggest=AutoSuggestFromHistory(),
        completer=command_completer,
        style=prompt_style,
        key_bindings=kb,
    )

    # 9. Interactive loop
    while True:
        try:
            # Get user input using prompt_toolkit
            # Use styled list for robust coloring
            user_input = await session.prompt_async(
                [
                    ("class:prompt", "You"),
                    ("", " › "),
                ],
                multiline=False,
                enable_history_search=True,
            )
            user_input = user_input.strip()

            if not user_input:
                continue

            # Handle special commands
            if user_input.startswith("/"):
                command = user_input.lower()
                
                if command in ["/exit", "/quit", "/q"]:
                    print(f"\n{Colors.GREEN}👋 Goodbye!{Colors.RESET}")
                    break
                elif command == "/help":
                    print_help()
                    continue
                elif command == "/clear":
                    print("\033[2J\033[H", end="")  # Clear screen
                    print_banner()
                    continue
                elif command == "/history":
                    print(f"{Colors.BRIGHT_CYAN}📝 Message History:{Colors.RESET}")
                    for i, msg in enumerate(agent.messages[1:], 1):  # Skip system message
                        role = msg.role.title()
                        content = msg.content[:100] + "..." if len(str(msg.content)) > 100 else str(msg.content)
                        print(f"  {i}. {role}: {content}")
                    print()
                    continue
                elif command == "/stats":
                    print_stats(agent, session_start)
                    continue
                else:
                    print(f"{Colors.YELLOW}⚠️  Unknown command: {user_input}{Colors.RESET}")
                    print_help()
                    continue

            # Add user message to agent
            agent.add_user_message(user_input)
            print(f"\n{Colors.BRIGHT_BLUE}🔍 Thinking...{Colors.RESET}")

            try:
                # Run agent with error handling
                response = await agent.run()
                
                # Display response
                if response.content:
                    print(f"\n{Colors.GREEN}🤖 Mini-Agent:{Colors.RESET}")
                    print(f"{Colors.RESET}{response.content}{Colors.RESET}")
                else:
                    print(f"\n{Colors.YELLOW}⚠️  No response generated{Colors.RESET}")

                print(f"\n{Colors.DIM}{'─' * 60}{Colors.RESET}\n")

            except Exception as e:
                print(f"\n{Colors.RED}❌ Error: {e}{Colors.RESET}")
                print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}\n")

        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}👋 Interrupted by user{Colors.RESET}")
            break
        except Exception as e:
            print(f"\n{Colors.RED}❌ Error: {e}{Colors.RESET}")
            print(f"{Colors.DIM}{'─' * 60}{Colors.RESET}\n")

    # 10. Cleanup MCP connections
    try:
        print(f"{Colors.BRIGHT_CYAN}Cleaning up MCP connections...{Colors.RESET}")
        await cleanup_mcp_connections()
        print(f"{Colors.GREEN}✅ Cleanup complete{Colors.RESET}\n")
    except Exception as e:
        print(f"{Colors.YELLOW}Error during cleanup (can be ignored): {e}{Colors.RESET}\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Mini-Agent - Interactive Agent Runtime",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mini-agent                          # Use current directory as workspace
  mini-agent --workspace /path/to/dir # Use specific workspace directory
        """,
    )
    parser.add_argument(
        "--workspace",
        "-w",
        default=None,
        help="Workspace directory (default: current directory)",
    )
    return parser.parse_args()


def main():
    """Main entry point for CLI"""
    # Parse command line arguments
    args = parse_args()

    # Determine workspace directory
    if args.workspace:
        workspace_dir = Path(args.workspace).absolute()
    else:
        # Use current working directory
        workspace_dir = Path.cwd()

    # Ensure workspace directory exists
    workspace_dir.mkdir(parents=True, exist_ok=True)

    # Run the agent (config always loaded from package directory)
    asyncio.run(run_agent(workspace_dir))


if __name__ == "__main__":
    main()
