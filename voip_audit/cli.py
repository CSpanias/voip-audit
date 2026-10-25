"""
Command-line interface for VoIP Audit.

VoIP Audit is a guided assessment tool that assists
security professionals in performing VoIP security
configuration reviews. The tool collects environment
information, conducts a structured control assessment,
and generates findings, remediation guidance, and
report outputs.
"""

import argparse

from rich.panel import Panel

from voip_audit.exporters.json import export_findings_json
from voip_audit.exporters.markdown import export_markdown
from voip_audit.review import run_assessment
from voip_audit.ui import console


def main() -> None:
    """
    Execute the VoIP security assessment workflow.
    """

    parser = argparse.ArgumentParser(
        description="Conduct VoIP security configuration reviews.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.parse_args()

    results = run_assessment()

    console.print()
    console.print(Panel.fit("[bold green]Assessment Complete[/bold green]"))
    console.print(f"[cyan]Responses:[/cyan] {len(results.responses)}")
    console.print(f"[red]Findings:[/red] {len(results.findings)}")
    console.print(f"[green]Positive Observations:[/green] {len(results.positives)}")

    export_findings_json(results, "voip-assessment.json")
    export_markdown(results, "voip-assessment.md")


if __name__ == "__main__":
    main()