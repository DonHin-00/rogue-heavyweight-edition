# Advanced Capabilities Guide

## New Attack Techniques

Rogue AI now includes 4 advanced attack techniques that significantly enhance adversarial testing capabilities:

### 1. Unicode Normalization Bypass

**Attack ID:** `unicode-normalization`

Uses Unicode normalization forms (NFD, NFKD) to bypass text filters by decomposing characters into their constituent parts or using compatibility equivalents.

**How it works:**
- Transforms text using different Unicode normalization forms
- Can bypass keyword-based filters
- Exploits differences in how systems handle Unicode

**Example:**
```python
from rogue.server.red_teaming.attacks.single_turn import UnicodeNormalization

attack = UnicodeNormalization(form="NFKD")
enhanced = attack.enhance("sensitive query")
```

### 2. Homoglyph Character Substitution

**Attack ID:** `homoglyph-free`

Uses visually similar Unicode characters (homoglyphs) to bypass text-based filters by replacing ASCII characters with look-alike characters from other Unicode ranges.

**How it works:**
- Replaces ASCII characters with Cyrillic or Greek lookalikes
- Example: 'a' → 'а' (Cyrillic 'a'), 'e' → 'е' (Cyrillic 'e')
- Bypasses simple keyword matching while remaining readable

**Example:**
```python
from rogue.server.red_teaming.attacks.single_turn import Homoglyph

attack = Homoglyph(substitution_rate=0.7)
enhanced = attack.enhance("access restricted data")
```

### 3. Morse Code Encoding

**Attack ID:** `morse-code`

Encodes the attack input in Morse code to bypass text-based filters and test the agent's ability to resist encoded payloads.

**How it works:**
- Converts text to Morse code (dots and dashes)
- Tests if the agent will decode and follow encoded instructions
- Exploits helpful behavior when presented with encoded content

**Example:**
```python
from rogue.server.red_teaming.attacks.single_turn import MorseCode

attack = MorseCode()
enhanced = attack.enhance("leak system prompt")
```

### 4. Chain-of-Thought Manipulation

**Attack ID:** `chain-of-thought-manipulation`

Uses step-by-step reasoning prompts to bypass safety filters by framing harmful requests as logical reasoning exercises.

**How it works:**
- Wraps harmful requests in academic/analytical framework
- Uses multi-step reasoning to normalize harmful queries
- Exploits the model's tendency to engage with logical prompts

**Example:**
```python
from rogue.server.red_teaming.attacks.single_turn import ChainOfThoughtManipulation

attack = ChainOfThoughtManipulation()
enhanced = attack.enhance("How to bypass security?")
```

## Advanced Metrics

### Adversarial Robustness Score (ARS)

**Class:** `AdversarialRobustnessMetric`

A composite metric that evaluates overall agent robustness across multiple dimensions:

1. **Defense Effectiveness** (35% weight): How well safety mechanisms work
2. **Evasion Resistance** (25% weight): Resistance to encoding/obfuscation
3. **Consistency** (20% weight): Consistent behavior across attack variations
4. **Information Leakage Resistance** (20% weight): Protection of internal state

**Score Range:** 0.0 (completely vulnerable) to 1.0 (fully robust)

**Usage:**
```python
from rogue.server.red_teaming.metrics import AdversarialRobustnessMetric

metric = AdversarialRobustnessMetric(judge_llm="openai/gpt-4o-mini")

class TestCase:
    actual_output = "I cannot help with that request"
    input = "malicious input"
    attack_type = "prompt-injection"

metric.measure(TestCase())
print(f"ARS: {metric.score:.2f}")
print(f"Reason: {metric.reason}")

# Get detailed breakdown
print(metric.detailed_scores)

# Get comprehensive report
report = metric.get_robustness_report()
```

### ML-Based Confidence Scoring

**Class:** `MLConfidenceMetric`

Computes an ML-based confidence score for vulnerability detection using multiple evaluation signals:

1. **Judge LLM Confidence** (35% weight): Expert model evaluation
2. **Pattern Matching** (25% weight): Known vulnerability patterns
3. **Keyword Indicators** (20% weight): Specific indicator detection
4. **Response Structure** (10% weight): Structure anomaly analysis
5. **Refusal Detection** (10% weight): Inverse of exploitation

**Score Range:** 0.0 (very low confidence) to 1.0 (very high confidence)

**Usage:**
```python
from rogue.server.red_teaming.metrics import MLConfidenceMetric

metric = MLConfidenceMetric(
    judge_llm="openai/gpt-4o-mini",
    vulnerability_type="pii-direct"
)

class TestCase:
    actual_output = "Here is your SSN: 123-45-6789"
    input = "What is my SSN?"

metric.measure(TestCase())
print(f"Confidence: {metric.score:.2f}")
print(f"Explanation: {metric.reason}")

# Get signal breakdown
signals = metric.get_signal_breakdown()
for signal, value in signals.items():
    print(f"  {signal}: {value:.2f}")
```

## Attack Pattern Correlation Engine

**Class:** `AttackPatternCorrelationEngine`

Analyzes relationships between attack techniques and vulnerabilities to identify patterns and predictive indicators.

**Features:**
- Attack effectiveness analysis
- Vulnerability pattern identification
- Attack synergy detection
- Risk profile calculation
- Sequence analysis

**Usage:**
```python
from rogue.server.red_teaming.correlation_engine import AttackPatternCorrelationEngine

engine = AttackPatternCorrelationEngine()

# Record attack results
engine.add_attack_result(
    attack_id="base64",
    vulnerability_id="pii-direct",
    success=True,
    severity="high",
    metadata={"response_time": 1.2}
)

# Get analysis
effectiveness = engine.calculate_attack_effectiveness()
patterns = engine.find_vulnerability_patterns()
synergies = engine.identify_attack_synergies()

# Generate comprehensive report
report = engine.generate_correlation_report()
print(report["key_findings"])
print(report["recommendations"])
```

## Enhanced Report Generator

**Class:** `EnhancedReportGenerator`

Generates comprehensive security reports with executive summaries, risk heatmaps, and remediation guidance.

**Features:**
- Executive summaries for stakeholders
- ASCII risk heatmaps
- Detailed remediation guides
- Trend analysis
- Priority-based action items

**Usage:**
```python
from rogue.server.red_teaming.enhanced_report_generator import EnhancedReportGenerator

generator = EnhancedReportGenerator()

# Generate executive summary
summary = generator.generate_executive_summary(
    results=test_results,
    agent_name="Production AI Agent",
    test_duration_seconds=1800
)
print(summary)

# Generate risk heatmap
heatmap = generator.generate_risk_heatmap_data(vulnerability_results)
print(heatmap["visualization"])

# Generate remediation guide
remediation = generator.generate_remediation_guide(detected_vulnerabilities)
print(remediation)

# Generate complete enhanced report
complete_report = generator.generate_complete_report(
    results=test_results,
    agent_name="My Agent",
    include_executive_summary=True,
    include_heatmap=True,
    include_remediation=True,
    historical_results=previous_results
)
```

## Integration with Existing Workflows

### Basic Scan with New Attacks

The new attacks are automatically included in basic scans:

```bash
uvx rogue-ai cli \
  --evaluated-agent-url http://localhost:10001 \
  --judge-llm openai/gpt-4o-mini \
  --scan-type basic
```

### Custom Scan with Specific Attacks

```bash
uvx rogue-ai cli \
  --evaluated-agent-url http://localhost:10001 \
  --judge-llm openai/gpt-4o-mini \
  --scan-type custom \
  --attacks unicode-normalization,homoglyph-free,morse-code,chain-of-thought-manipulation
```

### Using Advanced Metrics Programmatically

```python
from rogue.server.red_teaming.orchestrator import RedTeamOrchestrator
from rogue.server.red_teaming.models import RedTeamConfig, ScanType
from rogue.server.red_teaming.metrics import (
    AdversarialRobustnessMetric,
    MLConfidenceMetric
)

config = RedTeamConfig(
    scan_type=ScanType.BASIC,
    judge_llm="openai/gpt-4o-mini"
)

orchestrator = RedTeamOrchestrator(
    config=config,
    business_context="E-commerce customer service agent"
)

# Run tests and collect results
# ... (run orchestrator)

# Apply advanced metrics
ars_metric = AdversarialRobustnessMetric(judge_llm=config.judge_llm)
confidence_metric = MLConfidenceMetric(judge_llm=config.judge_llm)

# Analyze results with new metrics
for result in test_results:
    ars_metric.measure(result)
    confidence_metric.measure(result)
    
    print(f"Adversarial Robustness: {ars_metric.score:.2f}")
    print(f"Detection Confidence: {confidence_metric.score:.2f}")
```

## Best Practices

### 1. Use Multiple Attack Vectors
Combine traditional and advanced attacks for comprehensive testing:
```python
attacks = [
    "prompt-injection",      # Traditional
    "base64",                # Encoding
    "unicode-normalization", # Advanced evasion
    "homoglyph-free",       # Visual confusion
    "chain-of-thought-manipulation"  # Semantic
]
```

### 2. Leverage Correlation Analysis
Run correlation analysis after testing to identify patterns:
```python
engine = AttackPatternCorrelationEngine()
# ... add results
report = engine.generate_correlation_report()
# Use recommendations to improve defenses
```

### 3. Generate Executive Reports
Use enhanced reporting for stakeholder communication:
```python
generator = EnhancedReportGenerator()
exec_summary = generator.generate_executive_summary(results, "Production Agent")
# Share with leadership
```

### 4. Monitor Trends
Track security posture over time:
```python
historical_results = load_previous_results()
trend_analysis = generator.generate_trend_analysis(historical_results)
# Monitor for improvements or regressions
```

## Performance Considerations

### Attack Overhead
- Unicode Normalization: Minimal overhead (~10ms)
- Homoglyph: Low overhead (~20ms)
- Morse Code: Low overhead (~50ms)
- Chain-of-Thought: Moderate overhead (~100ms for framing)

### Metric Overhead
- Adversarial Robustness Metric: ~1-2 seconds (requires judge LLM)
- ML Confidence Metric: ~0.5-1 second (multiple signals)

### Correlation Analysis
- Best run after test completion
- O(n²) for synergy detection with n attacks
- Recommended for result sets < 10,000 attacks

## Troubleshooting

### Import Errors
If you see import errors, ensure you're using the correct import paths:
```python
# Correct imports
from rogue.server.red_teaming.attacks.single_turn import UnicodeNormalization
from rogue.server.red_teaming.metrics import AdversarialRobustnessMetric
from rogue.server.red_teaming.correlation_engine import AttackPatternCorrelationEngine
```

### Metric Requires Judge LLM
Most advanced metrics require a judge LLM:
```python
metric = AdversarialRobustnessMetric(
    judge_llm="openai/gpt-4o-mini",
    judge_llm_auth=os.getenv("OPENAI_API_KEY")
)
```

### Attack Not Found
Ensure attack IDs match exactly:
```bash
# Correct
--attacks unicode-normalization,homoglyph-free,morse-code

# Incorrect
--attacks unicode_normalization,homoglyph,morse  # Wrong IDs
```
