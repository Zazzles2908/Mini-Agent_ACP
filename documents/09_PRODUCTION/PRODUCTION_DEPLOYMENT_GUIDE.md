# 🏭 PRODUCTION DEPLOYMENT GUIDE

## From Development to Production: Complete Deployment Workflow

This guide provides a **comprehensive deployment strategy** for Mini-Agent in production environments.

---

## 🎯 DEPLOYMENT STRATEGIES

### **1. Local Development**
```bash
# Quick start for development
git clone <repository>
cd mini-agent

# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run locally
python -m mini_agent.cli
```

### **2. Docker Deployment**
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml .
RUN pip install -e .

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 miniagent && chown -R miniagent:miniagent /app
USER miniagent

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from mini_agent.config import get_config; get_config().health_check()"

# Run application
CMD ["python", "-m", "mini_agent.cli"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  mini-agent:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MINIMAX_API_KEY=${MINIMAX_API_KEY}
      - ZAI_API_KEY=${ZAI_API_KEY}
      - MINIMAX_DEBUG=false
      - MINIMAX_LOG_LEVEL=INFO
    volumes:
      - ./workspace:/app/workspace
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "from mini_agent.config import get_config; get_config().health_check()"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### **3. Kubernetes Deployment**
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mini-agent
  labels:
    app: mini-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mini-agent
  template:
    metadata:
      labels:
        app: mini-agent
    spec:
      containers:
      - name: mini-agent
        image: mini-agent:latest
        ports:
        - containerPort: 8080
        env:
        - name: MINIMAX_API_KEY
          valueFrom:
            secretKeyRef:
              name: mini-agent-secrets
              key: minimax-api-key
        - name: ZAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: mini-agent-secrets
              key: zai-api-key
        - name: MINIMAX_DEBUG
          value: "false"
        - name: MINIMAX_LOG_LEVEL
          value: "INFO"
        volumeMounts:
        - name: workspace-volume
          mountPath: /app/workspace
        - name: logs-volume
          mountPath: /app/logs
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: workspace-volume
        persistentVolumeClaim:
          claimName: mini-agent-workspace
      - name: logs-volume
        persistentVolumeClaim:
          claimName: mini-agent-logs

---
apiVersion: v1
kind: Service
metadata:
  name: mini-agent-service
spec:
  selector:
    app: mini-agent
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mini-agent-workspace
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mini-agent-logs
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
```

### **4. Cloud Deployment (AWS/GCP/Azure)**

#### **AWS ECS/Fargate**
```json
{
  "family": "mini-agent",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/miniAgentTaskRole",
  "containerDefinitions": [
    {
      "name": "mini-agent",
      "image": "ACCOUNT.dkr.ecr.REGION.amazonaws.com/mini-agent:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "MINIMAX_DEBUG",
          "value": "false"
        },
        {
          "name": "MINIMAX_LOG_LEVEL", 
          "value": "INFO"
        }
      ],
      "secrets": [
        {
          "name": "MINIMAX_API_KEY",
          "valueFrom": "arn:aws:ssm:REGION:ACCOUNT:parameter/mini-agent/minimax-api-key"
        },
        {
          "name": "ZAI_API_KEY", 
          "valueFrom": "arn:aws:ssm:REGION:ACCOUNT:parameter/mini-agent/zai-api-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/mini-agent",
          "awslogs-region": "REGION",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### **Google Cloud Run**
```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/mini-agent:latest', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/mini-agent:latest']
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'mini-agent'
      - '--image'
      - 'gcr.io/$PROJECT_ID/mini-agent:latest'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--set-env-vars'
      - 'MINIMAX_DEBUG=false,MINIMAX_LOG_LEVEL=INFO'
```

---

## 🔐 SECURITY CONFIGURATION

### **Environment Variables (Production)**
```bash
# Required API Keys (use secret management)
MINIMAX_API_KEY=<your_minimax_key>
ZAI_API_KEY=<your_zai_key>  # Optional

# Production Settings
MINIMAX_DEBUG=false
MINIMAX_LOG_LEVEL=WARNING
MINIMAX_MAX_STEPS=50
MINIMAX_WORKSPACE_DIR=/app/workspace

# Security
MINIMAX_ENABLE_CREDIT_PROTECTION=true
MINIMAX_MAX_TOOLS_PER_SESSION=100
```

### **Secret Management**

#### **AWS Secrets Manager**
```bash
# Create secrets
aws secretsmanager create-secret \
  --name mini-agent/minimax-api-key \
  --secret-string '{"api_key":"your_minimax_key"}'

aws secretsmanager create-secret \
  --name mini-agent/zai-api-key \
  --secret-string '{"api_key":"your_zai_key"}'
```

#### **Kubernetes Secrets**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mini-agent-secrets
type: Opaque
data:
  minimax-api-key: <base64_encoded_key>
  zai-api-key: <base64_encoded_key>
```

---

## 📊 MONITORING & OBSERVABILITY

### **Health Checks**
```python
# Add to your deployment
from mini_agent.config import get_config
from mini_agent.agent_factory import AgentFactory

@app.route('/health')
def health_check():
    try:
        config = get_config()
        health = config.health_check()
        return {
            'status': health['status'],
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }, 500
```

### **Prometheus Metrics**
```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest

# Metrics
REQUEST_COUNT = Counter('mini_agent_requests_total', 'Total requests')
REQUEST_DURATION = Histogram('mini_agent_request_duration_seconds', 'Request duration')
ACTIVE_SESSIONS = Gauge('mini_agent_active_sessions', 'Active sessions')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

### **Logging Configuration**
```python
import logging
import structlog

# Production logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

---

## 🚀 CI/CD PIPELINE

### **GitHub Actions**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -e .
        pip install pytest pytest-asyncio
    
    - name: Run tests
      run: pytest
    
    - name: Run production validation
      run: python simple_test.py

  security-scan:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security scan
      run: |
        pip install safety bandit
        safety check
        bandit -r mini_agent/

  deploy:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        # Your deployment commands here
        echo "Deploying to production..."
```

---

## 🔧 PRODUCTION OPTIMIZATIONS

### **Resource Limits**
```yaml
# Kubernetes resource limits
resources:
  requests:
    memory: "512Mi"
    cpu: "250m"
  limits:
    memory: "1Gi"
    cpu: "500m"
```

### **Auto-scaling**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: mini-agent-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: mini-agent
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### **Database/Storage Considerations**
```python
# For persistent storage
import aiosqlite

# Initialize database
async def init_db():
    async with aiosqlite.connect('/app/data/mini-agent.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data TEXT
            )
        ''')
        await db.commit()
```

---

## 📋 PRODUCTION CHECKLIST

### **Pre-Deployment**
- [ ] All tests passing (`python simple_test.py`)
- [ ] Security scan completed (no vulnerabilities)
- [ ] API keys configured in secret management
- [ ] Environment variables validated
- [ ] Resource limits configured
- [ ] Health checks implemented
- [ ] Logging configured
- [ ] Monitoring setup

### **Deployment**
- [ ] Container images built and tested
- [ ] Secrets configured in production environment
- [ ] Database migrations applied (if applicable)
- [ ] DNS/Load balancer configured
- [ ] SSL/TLS certificates installed
- [ ] Backup strategy implemented

### **Post-Deployment**
- [ ] Health checks passing
- [ ] Monitoring dashboards configured
- [ ] Alerting rules configured
- [ ] Performance baseline established
- [ ] Documentation updated
- [ ] Team notification setup

---

## 🎯 NEXT STEPS

1. **Choose your deployment strategy** based on your infrastructure
2. **Set up secret management** for API keys
3. **Configure monitoring and alerting**
4. **Implement CI/CD pipeline**
5. **Set up auto-scaling and backup**
6. **Document your specific configuration**

**This transforms your system from a development tool to a production-grade enterprise solution.**
