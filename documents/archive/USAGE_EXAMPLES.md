# Z.AI Optimized Integration Usage Examples

## Quick Start Examples

### 1. Basic Web Search
```python
from optimized_zai import OptimizedZAIClient
import asyncio

async def basic_search():
    zai = OptimizedZAIClient()
    result = await zai.advanced_web_search(
        query="artificial intelligence breakthrough",
        count=10
    )
    print(f"Found {result['count']} results")
    for item in result['results']:
        print(f"- {item['title']}")

asyncio.run(basic_search())
```

### 2. Web Search + Chat Analysis
```python
async def chat_search():
    zai = OptimizedZAIClient()
    result = await zai.web_search_in_chat(
        query="What are the latest AI developments?",
        model_name="glm-4.6"
    )
    print(f"Model: {result['model']}")
    print(f"Analysis: {result['response']}")

asyncio.run(chat_search())
```

### 3. Intelligent Web Reading
```python
async def read_webpage():
    zai = OptimizedZAIClient()
    result = await zai.intelligent_web_reading(
        url="https://example.com",
        format_type="markdown"
    )
    print(f"Title: {result['title']}")
    print(f"Content: {result['content'][:200]}...")

asyncio.run(read_webpage())
```

### 4. Research & Analysis
```python
async def research():
    zai = OptimizedZAIClient()
    result = await zai.research_and_analyze(
        query="machine learning trends 2025",
        depth="comprehensive"
    )
    print(f"Model: {result['model_used']}")
    print(f"Analysis: {result['analysis']}")

asyncio.run(research())
```

### 5. Intelligent Monitoring
```python
async def monitoring():
    zai = OptimizedZAIClient()
    monitor = ZAIMonitoringSystem(zai)
    
    monitor.add_intelligent_watch(
        name="AI Research",
        query="artificial intelligence breakthrough",
        interval_minutes=60,
        analysis_depth="comprehensive"
    )
    
    # Run one analysis cycle
    for watch in monitor.watches:
        result = await monitor.analyze_watch(watch)
        print(f"{watch['name']}: {result['model_used']}")

asyncio.run(monitoring())
```

### 6. Batch Research
```python
async def batch_research():
    zai = OptimizedZAIClient()
    queries = ["AI news", "tech trends", "cybersecurity"]
    results = await zai.batch_research(queries)
    print(f"Processed {results['successful']} queries")

asyncio.run(batch_research())
```

## Advanced Configuration

### Custom Search Parameters
```python
result = await zai.advanced_web_search(
    query="AI research",
    count=15,
    search_engine="search-prime",
    recency="oneWeek",
    domain_filter="arxiv.org",
    intent_prompt="Focus on recent breakthroughs"
)
```

### Multiple Analysis Depths
```python
# Quick analysis
result = await zai.research_and_analyze(
    query="AI trends",
    depth="quick"
)

# Deep analysis
result = await zai.research_and_analyze(
    query="AI trends", 
    depth="deep"
)
```

### Model Selection
```python
# Automatic selection
model = zai.select_model("complex reasoning")
print(model.name)  # glm-4.6

# Manual selection
model = zai.select_model("quick response")
print(model.name)  # glm-4-air
```

## Running the Integration

```bash
# Main integration with menu
python optimized_zai.py

# Direct usage examples shown above
```
