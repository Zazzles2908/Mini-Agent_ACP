# Example Configurations for Fact-Checking System

This directory contains example configurations and templates for using the fact-checking and self-assessment system.

---

## Quick Start Examples

### 1. Basic Text Validation

```bash
# Validate facts in a text document
python scripts/quick_validator.py text "Python is used by 85% of data scientists according to recent surveys."
```

### 2. File Validation

```bash
# Check if files exist and have valid syntax
python scripts/quick_validator.py files script.py requirements.txt README.md
```

### 3. Complete Assessment

```bash
# Comprehensive assessment of an implementation
python scripts/agent_integration.py quick "Create data processing script" script.py requirements.txt
```

---

## Configuration Files

### Assessment Configuration Template

Create `assessment_config.json`:

```json
{
  "task_description": "Create a web scraper for product data",
  "implementation_files": [
    "scraper.py",
    "requirements.txt",
    "README.md",
    "test_scraper.py"
  ],
  "requirements": [
    "Extract product names and prices",
    "Handle rate limiting",
    "Include error handling",
    "Provide usage documentation",
    "Support multiple product pages"
  ],
  "claims_to_verify": [
    "BeautifulSoup4 is the most popular Python web scraping library",
    "Rate limiting prevents IP blocking from most websites",
    "JSON format is suitable for product data storage"
  ]
}
```

Run with:
```bash
python scripts/agent_integration.py assess assessment_config.json
```

### Research Validation Configuration

Create `research_config.json`:

```json
{
  "task_description": "Research AI market trends",
  "text_content": "The global AI market is expected to reach $190 billion by 2025, with machine learning representing 60% of total investment.",
  "minimum_sources": 3,
  "required_topics": [
    "market size",
    "growth projections", 
    "investment trends",
    "key players"
  ]
}
```

---

## Example Workflows

### Workflow 1: Implementation Assessment

1. **Create the implementation**
2. **Prepare configuration**
3. **Run assessment**
4. **Review and improve**

```bash
# Step 1: Create your files (example)
echo "print('Hello World')" > example.py
echo "requests==2.28.0" > requirements.txt

# Step 2: Create assessment config
cat > my_assessment.json << EOF
{
  "task_description": "Create simple hello world script",
  "implementation_files": ["example.py", "requirements.txt"],
  "requirements": ["Print output", "Include dependencies"]
}
EOF

# Step 3: Run assessment
python scripts/agent_integration.py assess my_assessment.json

# Step 4: Review results
cat assessment_report.md
```

### Workflow 2: Research Validation

```bash
# Extract claims from research text
python scripts/quick_validator.py text "According to IEEE, Python ranks #1 in programming language popularity for 2023, with 48% of developers using it regularly."

# Generate comprehensive assessment
python scripts/agent_integration.py quick "Research Python popularity" --text "Your research content here" --files "research_notes.md sources.bib"
```

### Workflow 3: Continuous Integration

Add to your CI/CD pipeline:

```yaml
# .github/workflows/validate.yml
name: Validate Implementation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    
    - name: Run Assessment
      run: |
        python scripts/agent_integration.py quick "CI validation" implementation.py requirements.txt
```

---

## Integration Examples

### Python Integration

```python
from scripts.fact_checker import FactChecker, FunctionalTester, SelfAssessor

# Initialize components
fact_checker = FactChecker()
tester = FunctionalTester()
assessor = SelfAssessor()

# Validate your implementation
claims = fact_checker.extract_claims(your_text)
results = [fact_checker.verify_claim(claim) for claim in claims]

# Generate report
report = assessor.generate_assessment_report(
    task_description="Your task",
    fact_checks=results,
    test_results=[],
    metrics=assessor.calculate_quality_metrics(results, [], [])
)
print(report)
```

### Command Line Integration

```bash
#!/bin/bash
# build_and_validate.sh

echo "Building implementation..."
# Your build process here

echo "Running validation..."
python scripts/agent_integration.py quick "Build validation" \
  output_file.py \
  requirements.txt \
  documentation.md

echo "Validation complete. Check assessment_report.md for results."
```

---

## Customization Examples

### Custom Source Types

```python
from scripts.fact_checker import SourceType

# Define custom source weights
custom_weights = {
    SourceType.OFFICIAL: 0.98,    # Higher weight for official sources
    SourceType.REPUTABLE: 0.90,   # Higher weight for reputable sources
    SourceType.COMMUNITY: 0.70,   # Slightly higher for community
    SourceType.USER: 0.30         # Lower weight for user content
}
```

### Custom Testing Framework

```python
class CustomTester(FunctionalTester):
    def test_api_endpoint(self, endpoint_url: str) -> TestResult:
        """Custom test for API endpoints"""
        try:
            import requests
            response = requests.get(endpoint_url, timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}, Response time: {response.elapsed.total_seconds():.2f}s"
            return TestResult("API endpoint test", success, details)
        except Exception as e:
            return TestResult("API endpoint test", False, f"Error: {str(e)}")
```

### Custom Reporting

```python
def generate_custom_report(assessment_data: dict) -> str:
    """Generate custom report format"""
    metrics = assessment_data['metrics']
    
    # Custom template
    template = f"""
    🎯 IMPLEMENTATION REPORT
    ========================
    
    Task: {assessment_data['task_description']}
    Score: {metrics['overall_confidence']:.0f}/100
    Status: {assessment_data['overall_status']}
    
    Summary:
    - Accuracy: {metrics['accuracy_score']:.0f}%
    - Completeness: {metrics['completeness_score']:.0f}%
    - Quality: {['Poor', 'Fair', 'Good', 'Excellent'][int(metrics['overall_confidence']/25)]}
    """
    return template
```

---

## Best Practices

### 1. Before Running Assessment

- [ ] Complete your implementation
- [ ] Identify all factual claims
- [ ] Gather your sources
- [ ] Define clear requirements

### 2. During Assessment

- [ ] Review confidence levels carefully
- [ ] Pay attention to failed tests
- [ ] Check for unverified claims
- [ ] Note recommendations

### 3. After Assessment

- [ ] Address all critical issues
- [ ] Re-run assessment if major changes made
- [ ] Document lessons learned
- [ ] Update confidence scoring if needed

### 4. For Continuous Use

- [ ] Set up automated validation in CI/CD
- [ ] Track quality metrics over time
- [ ] Build team standards for confidence levels
- [ ] Regular review of source reliability

---

## Troubleshooting

### Common Issues

**"No factual claims detected"**
- Your text might not contain verifiable facts
- Try adding more specific claims with numbers or dates
- Check the claim extraction patterns

**"Low confidence scores"**
- Verify you're using reliable sources
- Cross-reference with additional sources
- Check source dates for currency

**"File syntax errors"**
- Ensure Python files have valid syntax
- Check for missing imports or dependencies
- Validate against PEP 8 standards

**"Missing requirements"**
- Review your requirements list
- Ensure implementation covers all specified features
- Add specific, measurable requirements

### Getting Help

1. Check the main documentation: `documents/FACT_CHECKING_SYSTEM.md`
2. Review example configurations in this directory
3. Run with `--format json` for detailed debugging output
4. Check the generated `assessment_report.md` for specific issues

---

*These examples provide a starting point for implementing the fact-checking system in various contexts. Customize them based on your specific needs and requirements.*