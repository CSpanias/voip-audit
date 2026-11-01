"""
Assessment workflow engine for VoIP security reviews.

This module contains the core assessment workflow logic and is responsible for:

- Collecting assessment context
- Selecting applicable audit questions
- Filtering controls by platform
- Coordinating the assessment workflow

The review engine is intentionally separated from reporting and export 
functionality to ensure the assessment logic remains independent from output 
formats.
"""


from rich.panel import Panel

from voip_audit.models import (
    AssessmentResults,
    AuditAnswer,
    ContextField,
    Finding,
    PositiveObservation,
    Question,
    QuestionResponse,
    ReviewContext,
    VoIPPlatform,
)
from voip_audit.loader import (
    load_context_fields,
    load_questions,
)
from voip_audit.ui import console


def get_fields_by_phase(
    fields: list[ContextField],
    phase: str,
) -> list[ContextField]:
    """
    Return context fields belonging to the specified phase.
    """

    return [
        field
        for field in fields
        if field.phase == phase
    ]


def get_applicable_context_fields(
    fields: list[ContextField],
    platform: VoIPPlatform,
) -> list[ContextField]:
    """
    Return context fields applicable to the selected
    VoIP platform.
    """

    applicable_fields = []

    for field in fields:

        if any(
            vendor.lower() == "all"
            for vendor in field.vendors
        ):
            applicable_fields.append(field)

        elif platform.value in field.vendors:
            applicable_fields.append(field)

    return applicable_fields


def get_applicable_questions(
    questions: list[Question],
    platform: VoIPPlatform,
) -> list[Question]:
    """
    Return all questions applicable to the selected platform.
    """

    applicable_questions = []

    for question in questions:

        if any(
            vendor.lower() == "all"
            for vendor in question.vendors
        ):
            applicable_questions.append(question)

        elif platform.value in question.vendors:
            applicable_questions.append(question)

    return applicable_questions


def collect_context(
    fields: list[ContextField],
    responses: dict | None = None,
    start: int = 1,
    overall_total: int | None = None,
) -> dict:
    """
    Collect assessment context information.

    Fields are presented dynamically based on the
    selected assessment phase and applicable VoIP
    platform.
    """

    responses = responses or {}

    context_notes = responses.pop("_context_notes", {})

    overall_total = overall_total or len(fields)

    for current, field in enumerate(fields, start=start):

        progress = max(
            1,
            int((current / overall_total) * 20),
        )

        bar = (
            f"[green]{'█' * progress}[/green]"
            f"[dim]{'░' * (20 - progress)}[/dim]"
        )

        console.print()
        console.print(
            f"[bold cyan][CONTEXT {current}/{overall_total}][/bold cyan] "
            f"{bar} "
            f"[bold]{field.label}[/bold]"
        )

        platform_hint = None

        if field.hints:

            platform_name = responses.get("voip_solution")

            if platform_name == VoIPPlatform.AUDIOCODES.value:
                platform_hint = field.hints.audiocodes

            elif platform_name == VoIPPlatform.OTHER.value:
                platform_hint = field.hints.other

            common_hint = field.hints.common

            if common_hint:
                console.print(
                    Panel.fit(
                        common_hint.strip(),
                        title="Evidence",
                        border_style="blue",
                    )
                )

            if platform_hint:
                console.print(
                    Panel.fit(
                        platform_hint.strip(),
                        title="Location",
                        border_style="yellow",
                    )
                )

        if field.type == "choice" and field.options:

            for index, option in enumerate(field.options, start=1):
                console.print(f"[cyan]{index}.[/cyan] {option}")

            while True:

                choice = input("> ").strip()

                try:
                    value = field.options[int(choice) - 1]
                    break

                except (ValueError, IndexError):
                    console.print("[red]Invalid selection.[/red]")

        else:
            value = input("> ").strip()

        if field.required:

            while not value:

                console.print("[red]This field is required.[/red]")
                value = input("> ").strip()

        if field.type == "integer":

            while True:

                try:
                    value = int(value)

                    if value < 0:
                        raise ValueError

                    break

                except ValueError:
                    console.print("[red]Please enter a valid number.[/red]")
                    value = input("> ").strip()

        console.print()
        console.print("[dim]Notes (optional)[/dim]")

        notes = input("> ").strip() or None

        if notes:
            context_notes[field.id] = notes

        responses[field.id] = value

    responses["_context_notes"] = context_notes

    return responses


def ask_question(
    question: Question,
    platform: VoIPPlatform,
    current: int,
    total: int,
) -> QuestionResponse:
    """
    Present a question to the assessor and record the response.
    """

    common_hint = None
    platform_hint = None

    if question.hints:
        common_hint = question.hints.common

        if platform == VoIPPlatform.AUDIOCODES:
            platform_hint = question.hints.audiocodes

        elif platform == VoIPPlatform.OTHER:
            platform_hint = question.hints.other

    console.print()

    progress = max(1, int((current / total) * 20))

    bar = (
        f"[green]{'█' * progress}[/green]"
        f"[dim]{'░' * (20 - progress)}[/dim]"
    )

    console.print(
        f"[bold cyan][{current}/{total}][/bold cyan] "
        f"{bar} "
        f"[bold]{question.question}[/bold]"
    )

    console.print()

    if common_hint:
        console.print(
            Panel.fit(
                common_hint.strip(),
                title="Evidence",
                border_style="blue",
            )
        )

    if platform_hint:
        console.print(
            Panel.fit(
                platform_hint.strip(),
                title="Location",
                border_style="yellow",
            )
        )

    console.print(
        Panel.fit(
            question.expected_value.strip(),
            title="Expected Value",
            border_style="green",
        )
    )

    console.print("1. Compliant")
    console.print("2. Non-Compliant")
    console.print("3. Not Applicable")
    console.print("4. Unknown")

    while True:
        choice = input("> ").strip()

        match choice:
            case "1":
                answer = AuditAnswer.COMPLIANT
                break

            case "2":
                answer = AuditAnswer.NON_COMPLIANT
                break

            case "3":
                answer = AuditAnswer.NOT_APPLICABLE
                break

            case "4":
                answer = AuditAnswer.UNKNOWN
                break

            case _:
                console.print(
                    "[red]Invalid selection.[/red]"
                )

    console.print("[bold]Notes (optional):[/bold]")
    notes = input("> ").strip() or None

    return QuestionResponse(
        finding_id=question.finding_id,
        answer=answer,
        notes=notes,
    )


def conduct_review(
    questions: list[Question],
    platform: VoIPPlatform,
) -> list[QuestionResponse]:
    """
    Execute the assessment question set.
    """

    responses = []

    total = len(questions)

    for current, question in enumerate(
        questions,
        start=1,
    ):
        response = ask_question(
            question,
            platform,
            current,
            total,
        )

        responses.append(response)

    return responses


def generate_findings(
    questions: list[Question],
    responses: list[QuestionResponse],
) -> list[Finding]:
    """
    Generate finding records for non-compliant controls.
    """

    findings = []

    questions_by_id = {
        question.finding_id: question
        for question in questions
    }

    for response in responses:
        question = questions_by_id[response.finding_id]

        if response.answer in (
            AuditAnswer.NOT_APPLICABLE,
            AuditAnswer.UNKNOWN,
        ):
            continue

        if response.answer != question.expected_answer:
            findings.append(
                Finding(
                    finding_id=question.finding_id,
                    theme=question.theme,
                    commentary_group=question.commentary_group,
                    section=question.section,
                    remediation_id=question.remediation_id,
                    title=question.finding_title,
                    description=question.description.strip(),
                    commentary=question.commentary.strip(),
                    solution=question.solution.strip(),
                    notes=response.notes,
                )
            )

    return findings


def generate_positive_observations(
    questions: list[Question],
    responses: list[QuestionResponse],
) -> list[PositiveObservation]:
    """
    Generate positive observations for compliant controls.
    """

    positives = []

    questions_by_id = {
        question.finding_id: question
        for question in questions
    }

    for response in responses:
        question = questions_by_id[response.finding_id]

        if response.answer in (
            AuditAnswer.NOT_APPLICABLE,
            AuditAnswer.UNKNOWN,
        ):
            continue

        if response.answer == question.expected_answer:
            positives.append(
                PositiveObservation(
                    finding_id=question.finding_id,
                    text=question.positive,
                    notes=response.notes,
                )
            )

    return positives


def build_assessment_results(
    context: ReviewContext,
    questions: list[Question],
    responses: list[QuestionResponse],
) -> AssessmentResults:
    """
    Build the final assessment results object.
    """

    findings = generate_findings(
        questions,
        responses,
    )

    positives = generate_positive_observations(
        questions,
        responses,
    )

    return AssessmentResults(
        context=context,
        findings=findings,
        positives=positives,
        responses=responses,
    )


def run_assessment() -> AssessmentResults:
    """
    Execute a complete VoIP security assessment.
    """

    all_fields = load_context_fields()

    setup_fields = get_fields_by_phase(all_fields, "setup")

    setup_responses = collect_context(setup_fields)

    platform = VoIPPlatform(setup_responses["voip_solution"])

    context_fields = get_applicable_context_fields(
        get_fields_by_phase(
            all_fields,
            "context",
        ),
        platform,
    )

    total_context_fields = (
        len(setup_fields)
        + len(context_fields)
    )

    context_responses = collect_context(
        context_fields,
        responses=setup_responses,
        start=len(setup_fields) + 1,
        overall_total=total_context_fields,
    )

    context_notes = {
        **setup_responses.pop("_context_notes", {}),
        **context_responses.pop("_context_notes", {}),
    }

    responses = {
        **setup_responses,
        **context_responses,
        "context_notes": context_notes,
    }

    context = ReviewContext(**responses)

    questions = get_applicable_questions(
        load_questions(),
        context.voip_solution,
    )

    responses = conduct_review(questions, context.voip_solution)

    return build_assessment_results(
        context=context,
        questions=questions,
        responses=responses,
    )