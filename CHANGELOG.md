# Changelog

All notable changes to the Rogue Heavyweight Edition will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.7] - 2025-02-10

### Added - Heavyweight Edition Features

#### Attack Techniques
- **Unicode Normalization Bypass** - Evade filters using Unicode decomposition (NFD, NFKD)
- **Homoglyph Character Substitution** - Visual confusion with lookalike characters from Cyrillic/Greek
- **Morse Code Encoding** - Payload obfuscation through Morse code encoding
- **Chain-of-Thought Manipulation** - Semantic attacks via reasoning frameworks

#### Metrics
- **Adversarial Robustness Score (ARS)** - Multi-dimensional security evaluation across 4 dimensions
- **ML Confidence Metric** - Multi-signal vulnerability detection with confidence scoring

#### Intelligence & Analysis
- **Attack Pattern Correlation Engine** - Identify attack synergies and patterns across test runs
- **Enhanced Report Generator** - Executive summaries, risk heatmaps, and remediation guides

#### All Attacks Now Free
- Converted all 39 attack techniques to free tier (previously 20 required premium)
- Includes 25 single-turn, 9 multi-turn, and 5 agentic attacks
- No QUALIFIRE_API_KEY required for any attacks

### Changed
- Updated basic scan to include 9 free attacks (was 5), adding Unicode normalization, homoglyphs, Morse code, and chain-of-thought manipulation
- Enhanced README with accurate attack counts (39 free attacks)
- Updated project description to reflect heavyweight edition capabilities
- Fixed broken documentation links
- Updated repository URLs to DonHin-00/rogue-heavyweight-edition
- Improved GitHub issue templates with heavyweight edition context
- Enhanced SDK documentation with heavyweight edition branding

### Documentation
- Added comprehensive ADVANCED_CAPABILITIES.md guide
- Created ENHANCEMENT_SUMMARY.md detailing all improvements
- Enhanced CHANGELOG.md (this file)
- Improved bug report and feature request templates
- Updated SDK README with heavyweight edition features

### Technical
- 69+ new test cases for advanced attacks and metrics
- All implementations follow existing patterns and conventions
- Zero security vulnerabilities (CodeQL validated)
- Full backward compatibility maintained

## [0.3.6] - Previous Release

### Features
- Initial Rogue AI Agent Evaluator & Red Team Platform
- 75+ vulnerabilities across 12 security categories
- CVSS-based risk scoring
- 8 compliance frameworks (OWASP, MITRE, NIST, GDPR, EU AI Act, ISO/IEC 42001, OWASP API)
- Support for A2A, MCP, and Python protocols
- Modern TUI with Go + Bubble Tea
- CLI for CI/CD integration
- Python SDK for programmatic access

---

For older versions, see the git history.
