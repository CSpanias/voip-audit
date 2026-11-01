"""
Markdown reporting functionality.

This exporter generates a consultant-facing assessment report containing an 
executive summary, commentary, and remediation guidance.
"""

from pathlib import Path

from voip_audit.constants import(
    THEMES, 
    THEME_DISPLAY,
    COMMENTARY_ORDER,
    COMMENTARY_SUMMARIES,
    COMMENTARY_INTROS,
    REMEDIATIONS,
    REFERENCES,
)
from voip_audit.models import AssessmentResults


def _get_review_scope(
    results: AssessmentResults,
) -> str:
    """
    Return a human-readable assessment scope.
    """

    return f"{results.context.voip_solution.value} deployment"

#-------------------------------------------------------------------------------
# EXECUTIVE SUMMARY
#-------------------------------------------------------------------------------

def _generate_assessment_context(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate the assessment context section.
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

    if context.deployment_type:
        lines.append(f"| Deployment Type | {context.deployment_type} |")

    if context.identity_provider:
        lines.append(f"| Identity Provider | {context.identity_provider} |")

    if context.sip_provider:
        lines.append(f"| SIP Provider | {context.sip_provider} |")

    if context.device_type:
        lines.append(f"| Device Type | {context.device_type} |")

    return lines


def _get_identified_themes(
    results: AssessmentResults,
) -> list[str]:

    identified = {finding.theme for finding in results.findings}

    return [theme for theme in THEMES if theme in identified]


def _get_security_posture(
    results: AssessmentResults,
) -> str:
    """
    Determine the overall security posture based on the ratio of positive 
    observations to findings.
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
    """

    lines = []

    posture = _get_security_posture(results)

    scope = _get_review_scope(results)

    themes = _get_identified_themes(results)

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
        "A Voice over Internal Protocol (VoIP) security configuration review "
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
    if themes:

        theme_text = _format_list(
            [
                THEME_DISPLAY.get(theme, theme.lower())
                for theme in themes
            ]
        )

        lines.append(
            f"The most significant observations related to "
            f"{theme_text}. Collectively, the identified "
            "weaknesses reduced assurance that administrative "
            "access, communications security, platform "
            "configuration, and monitoring controls were being "
            "implemented and governed in a consistent manner."
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
    Build a concise summary of the observations identified within a finding 
    group.

    The first sentence from each finding commentary is extracted, normalised, 
    de-duplicated, and combined into a single narrative statement for use 
    within the technical commentary section.
    """

    observations = []

    for finding in findings:

        sentence = (finding.commentary.strip().split(".")[0].strip())

        if (sentence and not sentence.split()[0].isupper()):

            sentence = sentence[0].lower() + sentence[1:]

        observations.append(sentence)

    observations = sorted(set(observations))

    return _format_list(observations)


def _build_group_commentary(
    group_name: str,
    findings: list,
) -> str:
    """
    Generate narrative commentary for a group of findings.
    """

    summary = COMMENTARY_SUMMARIES[group_name]

    intro = COMMENTARY_INTROS[group_name]

    observations = _get_observation_summary(
        findings
    )

    return (
        f"{summary} "
        f"{intro}{observations}."
    )


def _generate_commentary(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate the assessment commentary section.
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

    # Findings
    grouped_findings = _group_findings(results.findings)

    for group_name, findings in grouped_findings.items():

        lines.append(_build_group_commentary(group_name, findings))
        lines.append("")

    return lines

#-------------------------------------------------------------------------------
# REMEDIATION
#-------------------------------------------------------------------------------

def _generate_remediation(
    results: AssessmentResults,
) -> list[str]:
    """
    Generate the remediation section.
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

        recommendations = {}

        for finding in results.findings:

            remediation_id = getattr(
                finding,
                "remediation_id",
                None,
            )

            if remediation_id:
                recommendations.setdefault(
                    remediation_id,
                    REMEDIATIONS.get(
                        remediation_id,
                        f"[MISSING REMEDIATION] {finding.solution.strip()}",
                    ),
                )

            else:
                recommendations.setdefault(
                    finding.solution.strip(),
                    finding.solution.strip(),
                )

        for recommendation in sorted(recommendations.values()):

            lines.append(f"- {recommendation}")

        lines.append("")

    lines.append("### References")
    lines.append("")

    for title, url in REFERENCES["Generic"].items():
        lines.append(f"- [{url}]({url})")

    platform = results.context.voip_solution.value

    if platform in REFERENCES:
        for title, url in REFERENCES[platform].items():
            lines.append(f"- [{url}]({url})")


    return lines


def export_markdown(
    results: AssessmentResults,
    output_file: str,
) -> None:
    """
    Export assessment report as Markdown.
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