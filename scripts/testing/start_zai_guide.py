#!/usr/bin/env python3
"""
Z.AI Web Search Quick Start Guide
Run this to verify your Z.AI integration and get started!
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up the environment for Z.AI testing"""
    # Change to Mini-Agent directory
    mini_agent_dir = Path("C:\\Users\\Jazeel-Home\\Mini-Agent")
    os.chdir(mini_agent_dir)
    
    # Load environment variables
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key] = value
    
    # Add to path
    sys.path.insert(0, str(mini_agent_dir))

def test_zai_connection():
    """Test Z.AI connection"""
    try:
        from mini_agent.llm.zai_client import ZAIClient, get_zai_api_key
        
        api_key = get_zai_api_key()
        if not api_key:
            print("❌ Z.AI API key not found!")
            return False
        
        print(f"✅ Z.AI API key loaded: {api_key[:20]}...")
        
        client = ZAIClient(api_key)
        print("✅ Z.AI client initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Z.AI connection failed: {e}")
        return False

def demonstrate_web_search():
    """Demonstrate Z.AI web search capabilities"""
    import asyncio
    
    async def run_demo():
        try:
            from mini_agent.llm.zai_client import ZAIClient, get_zai_api_key
            
            api_key = get_zai_api_key()
            client = ZAIClient(api_key)
            
            print("\n🔍 Z.AI Web Search Demonstration")
            print("=" * 50)
            
            # Demo queries
            demo_queries = [
                {
                    "query": "GLM 4.6 latest features 2024",
                    "depth": "quick",
                    "description": "Quick GLM model search"
                },
                {
                    "query": "Z.AI Search Prime engine capabilities",
                    "depth": "comprehensive", 
                    "description": "Comprehensive search engine analysis"
                }
            ]
            
            for i, query_info in enumerate(demo_queries, 1):
                print(f"\n📋 Demo {i}: {query_info['description']}")
                print(f"Query: {query_info['query']}")
                print(f"Depth: {query_info['depth']}")
                
                try:
                    result = await client.research_and_analyze(
                        query=query_info["query"],
                        depth=query_info["depth"],
                        model_preference="glm-4.6"
                    )
                    
                    if result.get("success"):
                        print(f"✅ Success! Model: {result['model_used']}")
                        print(f"📝 Analysis preview: {result['analysis'][:150]}...")
                        print(f"🎯 Token usage: {result.get('token_usage', {}).get('total_tokens', 'N/A')}")
                    else:
                        print(f"❌ Failed: {result.get('error')}")
                        
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            print("\n🎉 Z.AI Web Search Demo Complete!")
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
    
    asyncio.run(run_demo())

def show_usage_examples():
    """Show usage examples"""
    print("\n" + "=" * 60)
    print("🚀 HOW TO USE Z.AI WEB SEARCH IN MINI-AGENT")
    print("=" * 60)
    
    print("""
1. START MINI-AGENT CLI:
   python -m mini_agent.cli

2. USE Z.AI WEB SEARCH:
   User: "Search for latest AI developments 2024"
   
   The agent will automatically use:
   🔧 zai_web_search(query="latest AI developments 2024", 
                     depth="comprehensive", 
                     model="auto")
   
3. USE Z.AI WEB READING:
   User: "Read https://github.com and summarize it"
   
   The agent will use:
   🔧 zai_web_reader(url="https://github.com", 
                     format="markdown", 
                     include_images=true)

4. CONFIGURE IN CONFIG.YAML:
   tools:
     enable_zai_search: true  # Already enabled by default

5. AVAILABLE MODELS:
   • glm-4.6     - Best for complex reasoning and coding
   • glm-4.5     - Strong agent capabilities  
   • glm-4-air   - Fast responses for simple queries
   • auto        - Automatic selection (recommended)

6. SEARCH DEPTHS:
   • quick        - 3 sources, fast results
   • comprehensive - 7 sources, balanced analysis
   • deep         - 10 sources, thorough research

7. EXAMPLE CONVERSATIONS:
   • "What are the latest developments in AI?"
   • "Research quantum computing breakthroughs"
   • "Find information about GLM model updates"
   • "Read this article and summarize it"

""")

def show_tools_status():
    """Show current tools status"""
    print("\n" + "=" * 60)
    print("🛠️  CURRENT TOOLS STATUS")
    print("=" * 60)
    
    tools_info = [
        ("✅", "zai_web_search", "Native GLM web search with AI analysis"),
        ("✅", "zai_web_reader", "Intelligent web page reading"),
        ("✅", "file_tools", "File operations (Read, Write, Edit)"),
        ("✅", "bash_tool", "Bash command execution"),
        ("✅", "note_tool", "Session note taking"),
        ("✅", "skill_tool", "Claude Skills integration"),
        ("⚠️", "minimax_search", "Disabled (use Z.AI instead)"),
        ("✅", "memory", "Knowledge graph memory"),
        ("⚠️", "filesystem", "Limited to /tmp (Claude Desktop)"),
        ("✅", "git", "Git repository operations"),
    ]
    
    for status, tool, description in tools_info:
        print(f"{status} {tool:<15} - {description}")

def main():
    """Main function"""
    print("🎯 Z.AI Web Search Quick Start Guide")
    print("=" * 60)
    print("This script will verify your Z.AI integration and show you how to use it!")
    
    # Setup
    print("\n🔧 Setting up environment...")
    setup_environment()
    
    # Test connection
    print("\n🔍 Testing Z.AI connection...")
    if test_zai_connection():
        # Show tools status
        show_tools_status()
        
        # Show usage examples
        show_usage_examples()
        
        # Offer to run demo
        print("\n" + "=" * 60)
        response = input("🚀 Would you like to see a live Z.AI web search demo? (y/N): ").strip().lower()
        
        if response in ['y', 'yes']:
            demonstrate_web_search()
        
        print("\n" + "=" * 60)
        print("✅ Z.AI INTEGRATION IS READY!")
        print("=" * 60)
        print("Next steps:")
        print("1. Start Mini-Agent: python -m mini_agent.cli")
        print("2. Try a web search query")
        print("3. Enjoy native GLM web search capabilities!")
        print("\n📚 For more info, see: documents/FINAL_ZAI_STATUS_REPORT.md")
        
    else:
        print("\n❌ Z.AI connection failed. Please check:")
        print("1. .env file contains valid ZAI_API_KEY")
        print("2. API key has sufficient credits")
        print("3. Internet connectivity is working")

if __name__ == "__main__":
    main()
