"""
Markdown reporting functionality.

This exporter generates a consultant-facing assessment report containing an 
executive summary, commentary, and remediation guidance.
"""

from pathlib import Path

from voip_audit.constants import(
    TITLE_REWRITES,
    POSITIVE_REWRITES,
    COMMENTARY_ORDER,
    COMMENTARY_SUMMARIES,
    THEME_REWRITES,
    COMMENTARY_INTROS,
)
from voip_audit.models import AssessmentResults


def _get_review_scope(
    results: AssessmentResults,
) -> str:
    """
    Return a human-readable description of the assessed VoIP deployment.

    This value is used within report narrative to describe the scope of
    the review in a consistent format.
    """

    return f"{results.context.voip_solution.value} deployment"

#-------------------------------------------------------------------------------
# EXECUTIVE SUMMARY
#-------------------------------------------------------------------------------

def _generate_assessment_context(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate the assessment context table.

    The context table summarises key characteristics of the assessed
    environment, including platform information, deployment details,
    management interfaces, authentication sources, and supporting
    infrastructure components.
    """


    context = results.context

    lines = []

    lines.append(
        "The assessed VoIP solution configuration is summarised below:"
    )
    lines.append("")

    lines.extend([
        "| Property | Value |",
        "|----------|-------|",
        f"| Organisation | {context.client_name} |",
        f"| VoIP Platform | {context.voip_solution.value} |",
    ])

    if context.platform_model:
        lines.append(f"| Platform Model | {context.platform_model} |")

    if context.software_version:
        lines.append(f"| Software Version | {context.software_version} |")

    if context.deployment_type:
        lines.append(f"| Deployment Type | {context.deployment_type} |")

    if context.management_address:
        lines.append(
            f"| Management Interfaces | {context.management_address} |"
        )

    if context.identity_provider:
        lines.append(f"| Identity Provider | {context.identity_provider} |")

    if context.sip_provider:
        lines.append(f"| SIP Provider | {context.sip_provider} |")

    if context.device_type:
        lines.append(f"| Device Type | {context.device_type} |")

    return lines


def _get_top_findings(
    results: AssessmentResults,
) -> list[str]:
    """
    Return a high-level summary of affected security themes.

    Findings are grouped by commentary category and translated into
    executive-summary-friendly themes to avoid listing individual
    configuration weaknesses.
    """

    groups = _group_findings(results.findings)

    return [
        THEME_REWRITES.get(
            group_name,
            group_name.lower(),
        )
        for group_name in groups
    ]


def _get_top_positives(
    results: AssessmentResults,
    limit: int = 4,
) -> list[str]:
    """
    Return a concise summary of positive security controls.

    Positive observations are rewritten into short descriptions suitable
    for inclusion within the executive summary.
    """

    items = []

    for positive in results.positives[:limit]:

        items.append(
            POSITIVE_REWRITES.get(
                positive.finding_id,
                positive.text.strip().rstrip(".").lower(),
            )
        )

    return sorted(set(items))


def _get_security_posture(
    results: AssessmentResults,
) -> str:
    """
    Determine the overall security posture of the assessed environment.

    The posture rating is derived from the ratio of positive observations
    to identified findings and is used to influence executive summary
    narrative and report messaging.
    """

    total = (len(results.findings) + len(results.positives))

    if total == 0:
        return "unknown"

    ratio = len(results.positives) / total

    if ratio >= 0.8:
        return "strong"

    if ratio >= 0.5:
        return "moderate"

    return "weak"


def _format_list(items: list[str]) -> str:
    """
    Format a list of values into a human-readable sentence fragment.

    Items are joined using natural language rules including appropriate
    use of commas and the final conjunction.
    """

    if not items:
        return ""

    if len(items) == 1:
        return items[0]

    if len(items) == 2:
        return f"{items[0]} and {items[1]}"

    return (
        ", ".join(items[:-1])
        + f", and {items[-1]}"
    )


def _generate_executive_summary(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate the executive summary section.

    The executive summary provides a management-level overview of the
    assessment scope, overall security posture, key areas of concern,
    positive observations, and the overall assessment conclusion.
    """

    lines = []

    posture = _get_security_posture(results)

    scope = _get_review_scope(results)

    lines.append("## Executive Summary")
    lines.append("")

    #---------------------------------------------------------------------------
    # Introductory Paragraph
    #---------------------------------------------------------------------------
    if posture == "strong":
        finding_summary = (
            "The assessed VoIP environment demonstrated a "
            "generally mature and well-managed security posture. However, "
            "a small number of opportunities were identified for improvement."
        )

    elif posture == "moderate":
        finding_summary = (
            "The assessed VoIP environment demonstrated a mixture of "
            "effective controls as well as opportunities for improvement."
        )

    else:
        finding_summary = (
            "The assessed VoIP environment demonstrated several "
            "weaknesses affecting the operation and enforcement of VoIP "
            "platform security controls."
        )

    lines.append(
        "A Voice over Internet Protocol (VoIP) security configuration review "
        f"was conducted for the {results.context.client_name} environment "
        f"covering the {scope}. The assessment considered authentication "
        "controls, cryptographic standards, access control mechanisms, "
        "monitoring capabilities, logging and audit controls, administrative "
        "security controls, and VoIP platform security controls. "
        f"{finding_summary}"
    )

    lines.append("")

    #---------------------------------------------------------------------------
    # Second Paragraph (High-Level Findings)
    #---------------------------------------------------------------------------
    top_findings = _get_top_findings(results)

    if top_findings:

        lines.append(
            "The most significant observations included "
            f"{_format_list(top_findings)}. Collectively, these issues reduced "
            "assurance that administrative access, communications security, "
            "monitoring controls, and privileged access management practices "
            "were operating effectively throughout the VoIP environment."
        )

        lines.append("")

    top_positives = _get_top_positives(results)

    if top_positives:

        lines.append(
            "The assessment also identified several positive security "
            f"practices, including {_format_list(top_positives)}."
        )

        lines.append("")

    #---------------------------------------------------------------------------
    # Conclusion
    #---------------------------------------------------------------------------
    if posture == "strong":
        lines.append(
            "Overall, the assessed configuration provided a generally "
            "effective foundation for secure VoIP operations. "
            "The opportunities identified do not indicate any significant "
            "weaknesses; however, addressing them would further improve the "
            "consistency and effectiveness of existing controls."
        )

    elif posture == "moderate":
        lines.append(
            "Overall, the VoIP platform provides a foundation for "
            "secure operation; however, further work is required to "
            "improve the consistency and effectiveness of key security "
            "controls. Addressing the observations identified would reduce "
            "security risk and strengthen assurance in the VoIP environment."
        )

    else:
        lines.append(
            "Overall, significant opportunities exist to strengthen the "
            "security posture of the VoIP environment. While the "
            "issues identified do not necessarily indicate an immediate "
            "compromise, they may reduce the effectiveness of controls "
            "intended to protect VoIP infrastructure. Priority should "
            "be given to improving authentication controls, strengthening "
            "access restrictions, and ensuring that security requirements "
            "are enforced consistently across VoIP infrastructure."
        )

    lines.append("")

    return lines

#-------------------------------------------------------------------------------
# COMMENTARY
#-------------------------------------------------------------------------------

def _generate_commentary_overview(
    results: AssessmentResults,
) -> str:
    """
    Generate a high-level overview of identified security themes.

    This summary introduces the commentary section and highlights the
    primary security domains in which opportunities for improvement
    were identified.
    """

    groups = _group_findings(results.findings)

    themes = []

    for group_name in groups:

        themes.append(
            THEME_REWRITES.get(
                group_name,
                group_name.lower(),
            )
        )

    return (
        "The assessment identified several opportunities to improve the "
        "security posture of the VoIP environment, primarily relating to "
        f"{_format_list(themes)}."
    )


def _generate_positive_observations(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate the positive observations subsection.

    Positive observations are included to highlight effective security
    controls and provide balanced reporting alongside identified
    findings.
    """


    if not results.positives:
        return []

    lines = []

    lines.append("### Positive Observations")
    lines.append("")

    lines.append(
        "The assessment also identified several positive security "
        "practices within the assessed VoIP environment:"
    )
    lines.append("")

    for finding in sorted(
        results.positives,
        key=lambda x: x.finding_id,
    ):
        lines.append(f"- {finding.text}")

    lines.append("")

    return lines


def _group_findings(
    findings,
) -> dict[str, list]:
    """
    Group findings by commentary group.

    Commentary groups are used to organise related findings into broader 
    reporting categories for technical commentary generation. The resulting 
    groups are returned in a predefined order to ensure report sections appear
    consistently regardless of the order in which findings were identified.
    """

    grouped = {}

    for finding in findings:

        group = getattr(finding, "commentary_group", None)

        if not group:
            continue

        grouped.setdefault(group, []).append(finding)

    ordered = {}

    for group in COMMENTARY_ORDER:
        if group in grouped:
            ordered[group] = grouped[group]

    return ordered


def _get_observation_summary(
    findings: list,
) -> str:
    """
    Generate a concise summary of findings within a commentary group.

    Individual findings are rewritten into report-friendly descriptions
    and merged into a single narrative sentence.
    """


    observations = []

    for finding in findings:

        observations.append(
            TITLE_REWRITES.get(
                finding.finding_id,
                finding.title.lower(),
            )
        )

    return _format_list(sorted(set(observations)))


def _build_group_commentary(
    group_name: str,
    findings: list,
) -> str:
    """
    Generate narrative commentary for a finding group.

    Commentary combines a security-domain introduction, a summary of
    identified observations, and supporting impact information to
    produce a consultant-style assessment narrative.
    """

    summary = COMMENTARY_SUMMARIES[group_name]
    intro = COMMENTARY_INTROS[group_name]

    observations = _get_observation_summary(findings)
    impact = _get_commentary_impact(findings)
    impact = impact.strip()

    return (
        f"{summary} "
        f"{intro}{observations}. "
        f"{impact}"
    )


def _get_commentary_impact(
    findings: list,
) -> str:
    """
    Combine finding impact statements into a single narrative block.

    Duplicate commentary entries are removed while preserving the
    original finding order.
    """

    impacts = []

    for finding in findings:

        impacts.append(finding.commentary.strip())

    return " ".join(dict.fromkeys(impacts))


def _generate_commentary(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate the assessment commentary section.

    The commentary section provides detailed technical narrative grouped
    by security theme, including contextual information, identified
    weaknesses, associated risks, and positive observations.
    """

    lines = []

    lines.append("## Commentary")
    lines.append("")

    lines.append(
        "A Voice over Internet Protocol (VoIP) security configuration review "
        f"was conducted for the {results.context.client_name} environment. The "
        "assessment reviewed the effectiveness of controls used to secure VoIP "
        "infrastructure, administrative interfaces, and supporting "
        "communications services."
    )

    lines.append("")

    # Context Table
    lines.extend(_generate_assessment_context(results))

    lines.append("")

    lines.append(_generate_commentary_overview(results))

    lines.append("")

    grouped_findings = _group_findings(results.findings)

    for group_name, findings in grouped_findings.items():

        lines.append(
            _build_group_commentary(
                group_name,
                findings,
            )
        )

        lines.append("")

    lines.extend(_generate_positive_observations(results))

    return lines

#-------------------------------------------------------------------------------
# REMEDIATION
#-------------------------------------------------------------------------------

def _generate_recommendations(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate a deduplicated list of remediation actions.

    Recommendations are derived directly from identified findings and
    consolidated to avoid repeating identical remediation guidance.
    """

    if not results.findings:
        return []

    lines = []
    seen = set()

    for finding in results.findings:

        recommendation = finding.solution.strip()

        if recommendation in seen:
            continue

        seen.add(recommendation)
        lines.append(f"- {recommendation}")

    lines.append("")

    return lines


def _generate_references(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate a finding-specific references section.

    References associated with identified findings are collected,
    deduplicated, and included to support remediation activities and
    provide links to relevant technical guidance.
    """

    references = []
    seen = set()

    platform = results.context.voip_solution.value.lower()

    for finding in results.findings:

        for url in finding.references.get(platform, []):

            if url not in seen:
                seen.add(url)
                references.append(url)

        for url in finding.references.get("generic", []):

            if url not in seen:
                seen.add(url)
                references.append(url)

    if not references:
        return []

    lines = []

    lines.append("### References")
    lines.append("")

    for url in references:
        lines.append(f"- {url}")

    lines.append("")

    return lines


def _generate_remediation(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate the remediation section.

    This section provides recommended corrective actions for identified
    findings and includes supporting technical references where
    available.
    """

    lines = []

    lines.append("## Remediation")
    lines.append("")

    if not results.findings:

        lines.append("No remediation actions are currently required.")
        lines.append("")

    else:

        lines.append("The following remediation actions are recommended:")
        lines.append("")

        lines.extend(_generate_recommendations(results))

    lines.extend(_generate_references(results))

    return lines


#-------------------------------------------------------------------------------
# EXPORT
#-------------------------------------------------------------------------------

def export_markdown(
    results: AssessmentResults,
    output_file: str,
) -> None:
    """
    Export the assessment results as a Markdown report.

    The generated report includes an executive summary, detailed
    commentary, remediation guidance, and supporting references.
    """

    path = Path(output_file)

    lines = [
        f"# {results.context.client_name} - VoIP Security Configuration Review",
        "",
    ]

    lines.extend(_generate_executive_summary(results))

    lines.extend(_generate_commentary(results))

    lines.extend(_generate_remediation(results))

    path.write_text("\n".join(lines), encoding="utf-8")