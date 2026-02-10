"""
Enhanced Report Generator with Executive Summaries and Risk Heatmaps.

Generates comprehensive security reports with:
- Executive summaries for stakeholders
- Risk heatmaps and visualizations
- Remediation recommendations
- Trend analysis
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from loguru import logger


class EnhancedReportGenerator:
    """
    Generates enhanced security reports with executive summaries,
    risk heatmaps, and detailed remediation guidance.
    """

    def __init__(self):
        """Initialize the report generator."""
        self.report_data: Dict[str, Any] = {}

    def generate_executive_summary(
        self,
        results: Dict[str, Any],
        agent_name: str = "Target Agent",
        test_duration_seconds: Optional[int] = None,
    ) -> str:
        """
        Generate an executive summary for stakeholders.

        Args:
            results: Red team test results
            agent_name: Name of the agent being tested
            test_duration_seconds: Duration of the test in seconds

        Returns:
            Markdown-formatted executive summary
        """
        total_vulnerabilities = results.get("total_vulnerabilities_tested", 0)
        detected_vulnerabilities = results.get("vulnerabilities_detected", 0)
        overall_score = results.get("overall_security_score", 0.0)
        critical_findings = results.get("critical_findings", [])
        high_findings = results.get("high_findings", [])

        # Calculate security posture
        if overall_score >= 0.8:
            posture = "**STRONG**"
            posture_color = "🟢"
        elif overall_score >= 0.6:
            posture = "**MODERATE**"
            posture_color = "🟡"
        elif overall_score >= 0.4:
            posture = "**WEAK**"
            posture_color = "🟠"
        else:
            posture = "**CRITICAL**"
            posture_color = "🔴"

        summary = f"""
# Executive Summary: {agent_name} Security Assessment

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

---

## Overall Security Posture: {posture_color} {posture}

**Security Score:** {overall_score:.1%}

### Key Metrics

| Metric | Value |
|--------|-------|
| Total Vulnerabilities Tested | {total_vulnerabilities} |
| Vulnerabilities Detected | {detected_vulnerabilities} |
| Detection Rate | {(detected_vulnerabilities / total_vulnerabilities * 100) if total_vulnerabilities > 0 else 0:.1f}% |
| Critical Issues | {len(critical_findings)} |
| High-Risk Issues | {len(high_findings)} |
"""

        if test_duration_seconds:
            minutes = test_duration_seconds // 60
            summary += f"| Test Duration | {minutes} minutes |\n"

        summary += "\n---\n\n"

        # Critical findings
        if critical_findings:
            summary += "## 🚨 Critical Findings\n\n"
            for i, finding in enumerate(critical_findings[:5], 1):
                vuln_id = finding.get("vulnerability_id", "Unknown")
                summary += f"{i}. **{vuln_id}**: {finding.get('description', 'No description')}\n"
            summary += "\n"

        # High-risk findings
        if high_findings:
            summary += "## ⚠️ High-Risk Findings\n\n"
            for i, finding in enumerate(high_findings[:5], 1):
                vuln_id = finding.get("vulnerability_id", "Unknown")
                summary += f"{i}. **{vuln_id}**: {finding.get('description', 'No description')}\n"
            summary += "\n"

        # Recommendations
        summary += "## 📋 Executive Recommendations\n\n"
        recommendations = self._generate_executive_recommendations(
            overall_score, len(critical_findings), len(high_findings)
        )
        for i, rec in enumerate(recommendations, 1):
            summary += f"{i}. {rec}\n"

        summary += "\n---\n\n"
        summary += "*For detailed technical analysis, see the full report below.*\n"

        return summary

    def generate_risk_heatmap_data(
        self, vulnerability_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate data for risk heatmap visualization.

        Args:
            vulnerability_results: List of vulnerability test results

        Returns:
            Heatmap data structure
        """
        # Group vulnerabilities by category and severity
        heatmap = {}

        for result in vulnerability_results:
            category = result.get("category", "Unknown")
            severity = result.get("severity", "low")
            detected = result.get("detected", False)

            if category not in heatmap:
                heatmap[category] = {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0,
                    "total": 0,
                    "detected": 0,
                }

            heatmap[category]["total"] += 1
            if detected:
                heatmap[category]["detected"] += 1
                heatmap[category][severity.lower()] += 1

        return {
            "heatmap_data": heatmap,
            "visualization": self._generate_ascii_heatmap(heatmap),
        }

    def _generate_ascii_heatmap(self, heatmap: Dict[str, Dict[str, int]]) -> str:
        """Generate ASCII art heatmap for terminal display."""
        if not heatmap:
            return "No data available for heatmap"

        output = "\n## Risk Heatmap by Category\n\n"
        output += "```\n"
        output += f"{'Category':<30} | Crit | High | Med  | Low  | Total\n"
        output += "-" * 70 + "\n"

        for category, counts in sorted(heatmap.items()):
            crit = counts.get("critical", 0)
            high = counts.get("high", 0)
            med = counts.get("medium", 0)
            low = counts.get("low", 0)
            total = counts.get("detected", 0)

            # Use blocks to visualize severity
            crit_bar = "█" * min(crit, 4)
            high_bar = "█" * min(high, 4)
            med_bar = "█" * min(med, 4)
            low_bar = "█" * min(low, 4)

            output += f"{category:<30} | {crit_bar:<4} | {high_bar:<4} | {med_bar:<4} | {low_bar:<4} | {total}\n"

        output += "```\n\n"
        return output

    def generate_remediation_guide(
        self, vulnerability_results: List[Dict[str, Any]]
    ) -> str:
        """
        Generate detailed remediation recommendations.

        Args:
            vulnerability_results: List of detected vulnerabilities

        Returns:
            Markdown-formatted remediation guide
        """
        guide = "## 🔧 Remediation Guide\n\n"

        # Group by priority
        critical = [v for v in vulnerability_results if v.get("severity") == "critical"]
        high = [v for v in vulnerability_results if v.get("severity") == "high"]
        medium = [v for v in vulnerability_results if v.get("severity") == "medium"]

        if critical:
            guide += "### 🔴 Critical Priority (Immediate Action Required)\n\n"
            for vuln in critical[:10]:
                guide += self._generate_remediation_item(vuln)

        if high:
            guide += "### 🟠 High Priority (Action Required Within 7 Days)\n\n"
            for vuln in high[:10]:
                guide += self._generate_remediation_item(vuln)

        if medium:
            guide += "### 🟡 Medium Priority (Action Required Within 30 Days)\n\n"
            for vuln in medium[:10]:
                guide += self._generate_remediation_item(vuln)

        return guide

    def _generate_remediation_item(self, vulnerability: Dict[str, Any]) -> str:
        """Generate a single remediation item."""
        vuln_id = vulnerability.get("vulnerability_id", "Unknown")
        vuln_name = vulnerability.get("name", vuln_id)
        category = vulnerability.get("category", "Unknown")

        item = f"#### {vuln_name}\n\n"
        item += f"- **Vulnerability ID:** {vuln_id}\n"
        item += f"- **Category:** {category}\n"

        # Get remediation recommendations based on vulnerability type
        recommendations = self._get_remediation_recommendations(vuln_id, category)

        item += f"- **Recommended Actions:**\n"
        for rec in recommendations:
            item += f"  - {rec}\n"

        item += f"\n"
        return item

    def _get_remediation_recommendations(
        self, vuln_id: str, category: str
    ) -> List[str]:
        """Get specific remediation recommendations for a vulnerability."""
        # Mapping of vulnerability patterns to recommendations
        recommendations_db = {
            "prompt-injection": [
                "Implement robust input validation and sanitization",
                "Use parameterized prompts with clear boundaries",
                "Add prompt injection detection filters",
                "Implement output validation to detect leaked instructions",
            ],
            "pii": [
                "Implement PII detection and masking in responses",
                "Add data access controls and audit logging",
                "Redact sensitive information before processing",
                "Implement user consent mechanisms for data handling",
            ],
            "sql-injection": [
                "Use parameterized queries exclusively",
                "Implement input validation with allowlists",
                "Apply principle of least privilege to database access",
                "Add SQL injection detection in input processing",
            ],
            "content-safety": [
                "Implement content filtering and moderation",
                "Add toxicity detection models",
                "Create safety classifiers for harmful content",
                "Establish clear content policies and enforce them",
            ],
            "bias": [
                "Audit training data for bias",
                "Implement fairness metrics and monitoring",
                "Add bias detection and mitigation layers",
                "Conduct regular bias testing across demographics",
            ],
        }

        # Try to match vulnerability to recommendation category
        for pattern, recs in recommendations_db.items():
            if pattern in vuln_id.lower() or pattern in category.lower():
                return recs

        # Default recommendations
        return [
            "Review and strengthen input validation",
            "Implement additional security controls",
            "Monitor and log suspicious activity",
            "Conduct follow-up security testing",
        ]

    def _generate_executive_recommendations(
        self, overall_score: float, critical_count: int, high_count: int
    ) -> List[str]:
        """Generate high-level recommendations for executives."""
        recommendations = []

        if critical_count > 0:
            recommendations.append(
                f"**URGENT:** Address {critical_count} critical "
                f"vulnerabilit{'y' if critical_count == 1 else 'ies'} immediately. "
                f"These pose severe security risks."
            )

        if high_count > 0:
            recommendations.append(
                f"Prioritize remediation of {high_count} high-risk "
                f"vulnerabilit{'y' if high_count == 1 else 'ies'} within 7 days."
            )

        if overall_score < 0.6:
            recommendations.append(
                "Overall security posture requires significant improvement. "
                "Consider comprehensive security hardening."
            )

        if overall_score >= 0.8:
            recommendations.append(
                "Maintain current security posture through regular testing "
                "and monitoring."
            )
        else:
            recommendations.append(
                "Implement continuous security testing and establish "
                "security metrics dashboard."
            )

        recommendations.append(
            "Schedule follow-up security assessment in 30 days to verify "
            "remediation effectiveness."
        )

        return recommendations

    def generate_trend_analysis(
        self, historical_results: List[Dict[str, Any]]
    ) -> str:
        """
        Generate trend analysis from historical test results.

        Args:
            historical_results: List of previous test results

        Returns:
            Markdown-formatted trend analysis
        """
        if len(historical_results) < 2:
            return "## Trend Analysis\n\nInsufficient historical data for trend analysis.\n"

        analysis = "## 📊 Trend Analysis\n\n"

        # Extract metrics over time
        dates = []
        scores = []
        vuln_counts = []

        for result in historical_results:
            dates.append(result.get("date", "Unknown"))
            scores.append(result.get("overall_security_score", 0.0))
            vuln_counts.append(result.get("vulnerabilities_detected", 0))

        # Calculate trends
        score_trend = "improving" if scores[-1] > scores[0] else "declining"
        vuln_trend = (
            "decreasing" if vuln_counts[-1] < vuln_counts[0] else "increasing"
        )

        analysis += f"### Security Score Trend: **{score_trend.upper()}**\n\n"
        analysis += f"- Initial Score: {scores[0]:.1%}\n"
        analysis += f"- Latest Score: {scores[-1]:.1%}\n"
        analysis += f"- Change: {(scores[-1] - scores[0]):.1%}\n\n"

        analysis += f"### Vulnerability Detection Trend: **{vuln_trend.upper()}**\n\n"
        analysis += f"- Initial Count: {vuln_counts[0]}\n"
        analysis += f"- Latest Count: {vuln_counts[-1]}\n"
        analysis += f"- Change: {vuln_counts[-1] - vuln_counts[0]:+d}\n\n"

        return analysis

    def generate_complete_report(
        self,
        results: Dict[str, Any],
        agent_name: str = "Target Agent",
        include_executive_summary: bool = True,
        include_heatmap: bool = True,
        include_remediation: bool = True,
        historical_results: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Generate a complete enhanced security report.

        Args:
            results: Red team test results
            agent_name: Name of the agent
            include_executive_summary: Whether to include executive summary
            include_heatmap: Whether to include risk heatmap
            include_remediation: Whether to include remediation guide
            historical_results: Optional historical results for trend analysis

        Returns:
            Complete markdown-formatted report
        """
        report = ""

        # Executive Summary
        if include_executive_summary:
            report += self.generate_executive_summary(results, agent_name)
            report += "\n\n---\n\n"

        # Risk Heatmap
        if include_heatmap:
            vuln_results = results.get("vulnerability_results", [])
            heatmap_data = self.generate_risk_heatmap_data(vuln_results)
            report += heatmap_data.get("visualization", "")
            report += "\n\n---\n\n"

        # Trend Analysis
        if historical_results:
            report += self.generate_trend_analysis(historical_results)
            report += "\n\n---\n\n"

        # Remediation Guide
        if include_remediation:
            detected_vulns = [
                v
                for v in results.get("vulnerability_results", [])
                if v.get("detected", False)
            ]
            if detected_vulns:
                report += self.generate_remediation_guide(detected_vulns)
                report += "\n\n---\n\n"

        # Detailed Results (existing report format would go here)
        report += "## Detailed Technical Results\n\n"
        report += "*See full technical report for detailed attack logs and responses.*\n"

        return report
