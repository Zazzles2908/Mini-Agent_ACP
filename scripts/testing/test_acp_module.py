"""Test ACP module availability."""
try:
    import acp
    print("✅ acp module available")
    if hasattr(acp, "__version__"):
        print(f"   Version: {acp.__version__}")
    else:
        print("   Version: unknown")
    print(f"   Module path: {acp.__file__}")
except ImportError as e:
    print("❌ acp module not found")
    print(f"   Error: {e}")
    print("\n💡 Solution:")
    print("   Install with: pip install agent-client-protocol")
