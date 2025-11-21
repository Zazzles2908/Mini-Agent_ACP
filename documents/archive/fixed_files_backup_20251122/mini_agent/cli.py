"""CLI module for mini-agent"""

import sys
import asyncio
from typing import List
from . import Config, LLMClient, LLMProvider, Message


def main():
    """Main CLI entry point"""
    print("Mini-Agent CLI - Version 0.1.0")
    print("This is a lightweight AI agent framework")
    print()
    
    # Check if we have any arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "test":
            asyncio.run(test_config())
        elif command == "chat":
            asyncio.run(start_chat())
        else:
            print(f"Unknown command: {command}")
            print("Available commands: test, chat")
    else:
        print("No command specified. Available commands:")
        print("  test  - Test configuration")
        print("  chat  - Start interactive chat")


async def test_config():
    """Test the configuration"""
    print("=== Testing Mini-Agent Configuration ===")
    
    try:
        # Load configuration
        print("📝 Loading configuration...")
        config = Config.load()
        print("✅ Configuration loaded successfully")
        
        # Initialize LLM client
        print("🔧 Initializing LLM client...")
        llm_client = LLMClient(
            api_key=config.llm.api_key,
            provider=config.llm.provider,
            api_base=config.llm.api_base,
            model=config.llm.model
        )
        print("✅ LLM client initialized")
        
        # Test with a simple message
        print("🧪 Testing with sample message...")
        test_message = Message(
            role="user", 
            content="Hello! This is a test message. Please respond with 'Mini-Agent is working!'"
        )
        
        response = await llm_client.chat([test_message])
        print(f"✅ API call successful!")
        print(f"Response: {response.content}")
        print(f"Model: {response.model}")
        print(f"Finish reason: {response.finish_reason}")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        import traceback
        traceback.print_exc()


async def start_chat():
    """Start interactive chat"""
    print("=== Mini-Agent Interactive Chat ===")
    print("Type 'quit' or 'exit' to end the session")
    print()
    
    try:
        # Load configuration
        config = Config.load()
        
        # Initialize LLM client
        llm_client = LLMClient(
            api_key=config.llm.api_key,
            provider=config.llm.provider,
            api_base=config.llm.api_base,
            model=config.llm.model
        )
        
        # Chat loop
        messages = []
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Mini-Agent: Goodbye! 👋")
                    break
                
                if not user_input:
                    continue
                
                # Add user message
                user_message = Message(role="user", content=user_input)
                messages.append(user_message)
                
                # Get response
                print("Mini-Agent: Thinking...", end="", flush=True)
                response = await llm_client.chat(messages)
                print("\r" + " " * 25 + "\r", end="")  # Clear "Thinking..." text
                
                print(f"Mini-Agent: {response.content}")
                
                # Add assistant response to conversation
                assistant_message = Message(role="assistant", content=response.content)
                messages.append(assistant_message)
                
            except KeyboardInterrupt:
                print("\n\nMini-Agent: Chat interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to start chat: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()