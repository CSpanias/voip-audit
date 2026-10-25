"""
JSON export functionality.

This exporter generates machine-readable output intended
for consumption by downstream tooling such as XML
converters and reporting pipelines.
"""

import json
from pathlib import Path

from vpn_audit.models import AssessmentResults


def export_findings_json(
    results: AssessmentResults,
    output_file: str,
) -> None:
    """
    Export findings in the standard findings format.
    """

    findings = [
        {
            "id": "voip-audit",
            "title": "VoIP Security Configuration Review",
            "description": (
                "A security configuration review of the organisation's "
                "VoIP platform was performed."
            ),
            "platform": results.context.voip_solution.value,
        }
    ]

    findings.extend(
        [
            {
                "id": finding.finding_id,
                "title": finding.title,
                "description": finding.description,
            }
            for finding in results.findings
        ]
    )

    path = Path(output_file)

    with path.open("w", encoding="utf-8") as file:
        json.dump(
            {"findings": findings},
            file,
            indent=4,
        )