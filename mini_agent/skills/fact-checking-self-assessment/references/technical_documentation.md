# Fact-Checking Skill Reference Documentation

## Technical Architecture

### Core Components

1. **FactChecker Class**
   - `extract_claims()`: Pattern-based claim extraction from text
   - `verify_claim()`: Multi-source verification with confidence scoring
   - Source classification: Official, Reputable, Community, User

2. **FunctionalTester Class**
   - `test_file_existence()`: Validate file presence
   - `test_code_syntax()`: Python syntax validation
   - `test_requirements_coverage()`: Requirements validation

3. **SelfAssessor Class**
   - `calculate_quality_metrics()`: Comprehensive scoring (0-100)
   - `generate_assessment_report()`: Professional reporting
   - Confidence-based recommendations

### Confidence Scoring System

- **Official Sources**: 95% reliability weight
- **Reputable Sources**: 85% reliability weight  
- **Community Sources**: 60% reliability weight
- **User Sources**: 40% reliability weight

### Quality Metrics

- **Accuracy Score**: Factual correctness (0-100)
- **Completeness Score**: Requirements coverage (0-100)
- **Functionality Score**: Working implementation (0-100)
- **Reliability Score**: Consistency and stability (0-100)
- **Overall Confidence**: Weighted average of all scores

### Validation Thresholds

- **High Confidence** (90-100%): Production ready
- **Medium Confidence** (70-89%): Review recommended
- **Low Confidence** (50-69%): Improvements needed
- **Review Required** (<50%): Major issues identified

## API Integration

### Claim Extraction Patterns

The system uses regex patterns to identify factual claims:

```python
patterns = [
    r"([A-Z][^.!?]*(?:according to|research shows|studies indicate|evidence suggests)[^.!?]*[.!?])",
    r"([A-Z][^.!?]*(?:is|are|was|were)[^.!?]*(?:the|most|a|an)?[^.!?]*(?:popular|common|widely|most)[^.!?]*[.!?])",
    r"([A-Z][^.!?]*(?:[0-9]+(?:\.[0-9]+)?(?:\s*%|\s*percent|\s*people|\s*users|\s*cases)[^.!?]*)[.!?])",
    r"([A-Z][^.!?]*(?:it has been shown|it is known|research indicates|studies show)[^.!?]*[.!?])",
]
```

### Web Integration Points

The skill integrates with:
- Z.AI native web search capabilities
- Mini-Agent's fact-checking tools
- Session note system for tracking assessments

## Usage Patterns

### Basic Assessment Workflow

1. **Extract Claims**: Use pattern matching to identify factual statements
2. **Verify Sources**: Cross-reference against reliable sources
3. **Test Functionality**: Validate implementation completeness
4. **Calculate Metrics**: Generate quality scores and confidence levels
5. **Generate Report**: Create professional assessment documentation

### Integration with Mini-Agent Workflows

The skill integrates with Mini-Agent's:
- Tool system for validation
- Documentation standards for reporting
- Session management for context preservation
- Quality assurance processes

## Implementation Details

### Error Handling

- Graceful fallback for missing web sources
- Unicode encoding compatibility
- Missing file handling
- Invalid syntax detection

### Performance Considerations

- Efficient regex pattern matching
- Minimal resource usage
- Optimized for real-time assessment
- Scalable to large text volumes

### Security and Privacy

- No external API key requirements for core functionality
- Local source validation for sensitive content
- Secure assessment logging
- Privacy-preserving fact verification

## Troubleshooting

### Common Issues

1. **No Claims Detected**
   - Check text content for factual statements
   - Verify regex patterns are appropriate
   - Ensure minimum claim length requirements

2. **Low Confidence Scores**
   - Add more specific source references
   - Include authoritative documentation
   - Cross-verify with multiple sources

3. **Missing Requirements**
   - Review requirements specification
   - Check implementation completeness
   - Validate against expected outcomes

### Debug Mode

Enable detailed logging by setting environment variables:
- `FACT_CHECK_VERBOSE=true` for detailed output
- `FACT_CHECK_DEBUG=true` for diagnostic information

## Future Enhancements

### Planned Improvements

1. **Enhanced Pattern Recognition**: More sophisticated claim extraction
2. **Real-time Web Verification**: Direct integration with web APIs
3. **Machine Learning Integration**: Improved accuracy through ML models
4. **Custom Domain Support**: Specialized validation for specific domains

### Extensibility

The skill architecture supports:
- Custom source types and weights
- Domain-specific validation rules
- Integration with external assessment systems
- Plugin architecture for specialized tools