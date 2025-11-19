# Manual Deployment Guide for Supabase Schema

## 🚨 **MANUAL STEP REQUIRED**

**Current Status**: Schema files ready, Docker stack running, waiting for manual deployment

### **Step 1: Deploy Main Schema**

1. **Open Supabase Dashboard**
   - Go to: https://mxaazuhlqewmkweewyaz.supabase.co
   - Navigate to SQL Editor

2. **Execute Main Schema**
   - Copy content from: `C:\Users\Jazeel-Home\.mini-agent\observability\DEPLOY_SCHEMA.sql`
   - Paste into SQL Editor
   - Click "Run" button
   - **Expected Result**: 4 tables created in `mini_agent_observability` schema

3. **Verify Deployment**
   - Check Tables section for new tables:
     - `mini_agent_observability.traces`
     - `mini_agent_observability.tool_executions`
     - `mini_agent_observability.performance_metrics`
     - `mini_agent_observability.decisions`

### **Step 2: Deploy Public Views**

1. **Execute Views Script**
   - Copy content from: `C:\Users\Jazeel-Home\.mini-agent\observability\DEPLOY_VIEWS.sql`
   - Paste into SQL Editor
   - Click "Run" button

2. **Verify Views**
   - Check Tables section for new views:
     - `public.agent_traces`
     - `public.agent_tool_executions`
     - `public.agent_performance_metrics`
     - `public.agent_decisions`

### **Step 3: Test Deployment**

After completing Steps 1 & 2, run:
```bash
cd C:\Users\Jazeel-Home\.mini-agent\observability
python test_post_deployment.py
```

**Expected Output**: "SUCCESS: Observability system ready for Mini-Agent integration!"

### **Step 4: Langfuse Setup**

1. **Access Langfuse**
   - Go to: http://localhost:3000
   - Create account/project if needed

2. **Obtain API Keys**
   - Get `LANGFUSE_SECRET_KEY` and `LANGFUSE_PUBLIC_KEY`
   - Save these for environment configuration

### **Current Docker Status**
```
✅ observability-db-1: Running (healthy) 
✅ observability-langfuse-server-1: Running
```

**Next**: Complete manual Supabase deployment → Test → Proceed to Phase 2
