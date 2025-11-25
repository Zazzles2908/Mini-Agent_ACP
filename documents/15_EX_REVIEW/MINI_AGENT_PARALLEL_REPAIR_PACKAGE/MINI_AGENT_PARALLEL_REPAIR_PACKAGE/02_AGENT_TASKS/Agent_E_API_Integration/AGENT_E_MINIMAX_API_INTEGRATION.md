# Agent E: MiniMax-Coding-MCP Real API Integration
*Priority: MEDIUM - Replace simulations with actual API calls*

## 🎯 Mission
Transform MiniMax coding MCP server from simulation functions to real GLM-4.6 API integration.

## 📋 Current Problem
- **Issue:** MCP server uses `simulate_*` functions instead of real API
- **Impact:** Generated code is placeholder/templated, not AI-generated
- **Current State:** 4 tools available but using fake data
- **Required:** Real GLM-4.6 model integration

## 🛠️ Implementation Steps

### Step 1: API Integration Setup
**Update:** `scripts/mcp_servers/minimax_coding_plan_mcp_server.py`

**Replace Simulations:**
```python
# REMOVE: simulate_code_generation()
# REMOVE: simulate_code_analysis()  
# REMOVE: simulate_plan_creation()
# REMOVE: simulate_code_review()

# ADD: Real MiniMax API calls
async def call_minimax_api(prompt: str, model: str = "glm-4.6") -> str:
    # Implementation using GLM-4.6 endpoint
```

### Step 2: API Authentication & Endpoint
**Configuration:**
```python
API_BASE_URL = "https://api.minimax.ai"  # or appropriate endpoint
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY")

# Headers for API calls
headers = {
    "Authorization": f"Bearer {MINIMAX_API_KEY}",
    "Content-Type": "application/json"
}
```

### Step 3: Implement Real Tool Functions
**Update Each Tool:**

1. **`minimax_generate_code`:**
   ```python
   async def minimax_generate_code(description, language, framework=None):
       prompt = f"Generate {language} code for: {description}"
       if framework: prompt += f" using {framework}"
       response = await call_minimax_api(prompt)
       return format_generated_code(response)
   ```

2. **`minimax_analyze_code`:**
   ```python
   async def minimax_analyze_code(code, analysis_type, language):
       prompt = f"Analyze this {language} code for {analysis_type}: {code}"
       response = await call_minimax_api(prompt)
       return format_analysis(response)
   ```

3. **`minimax_create_plan`:**
   ```python
   async def minimax_create_plan(project_description, complexity, ...):
       prompt = f"Create development plan for: {project_description}"
       response = await call_minimax_api(prompt)
       return format_plan(response)
   ```

4. **`minimax_review_code`:**
   ```python
   async def minimax_review_code(code, language, focus_areas=None):
       prompt = f"Review this {language} code" 
       if focus_areas: prompt += f" focusing on: {', '.join(focus_areas)}"
       response = await call_minimax_api(prompt)
       return format_review(response)
   ```

### Step 4: Error Handling & Rate Limits
**Add Robust Error Handling:**
```python
async def call_minimax_api_with_retry(prompt: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            response = await api_call(prompt)
            return response
        except RateLimitError:
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
        except APIError as e:
            return f"API Error: {str(e)}"
    return "Failed after retries"
```

### Step 5: Testing & Validation
```python
# Test real API integration
async def test_real_api():
    result = await minimax_generate_code(
        description="Create a simple calculator function", 
        language="python"
    )
    print("Real API Result:", result[:200], "...")

# Compare vs simulation results
```

## 📁 Resources
- **Current Server:** `scripts/mcp_servers/minimax_coding_plan_mcp_server.py`
- **API Docs:** Based on GLM-4.6 documentation
- **Simulation Functions:** Current fake implementations to replace

## 🎯 Success Criteria
**Complete when:**
- All 4 MiniMax tools use real GLM-4.6 API
- Generated code is AI-created, not templated
- API authentication works reliably  
- Error handling prevents crashes
- Tools provide real AI analysis/review

## ⏱️ Estimated Time
**Target:** 8-10 hours
**Max:** 12 hours

## 🎯 Expected Outcomes

**Before Integration:**
```
❌ Generated code: "Here's a simple Python function..." 
❌ Analysis: "The code follows good patterns..."
❌ Placeholder responses, not AI-generated
```

**After Integration:**
```
✅ Generated code: Real AI-generated implementation
✅ Analysis: Actual AI code review and suggestions  
✅ Plan: AI-created development roadmap
✅ Review: Genuine AI code assessment
```

## ⚠️ Important Notes
- **API Costs:** Monitor GLM-4.6 usage and costs
- **Rate Limits:** Implement proper throttling
- **Error Handling:** Graceful fallbacks for API failures
- **Output Quality:** Verify AI-generated content is useful
- **Testing:** Test each tool individually before integration
