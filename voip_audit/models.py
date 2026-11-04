"""
Core data models used throughout the VoIP Audit application.

This module defines the strongly-typed data structures that represent:

- Assessment questions
- Review context collected from the client
- Assessor responses
- Audit findings
- Positive observations
- Final assessment results

The models are implemented using Pydantic and provide validation for data 
loaded from YAML files and generated during the audit workflow.

These models form the contract between the review engine and all exporters, 
ensuring a consistent and predictable data structure throughout the application.
"""

from enum import Enum

from pydantic import BaseModel, Field


class VoIPPlatform(str, Enum):
    """
    Supported VoIP platforms.

    Used for displaying platform-specific navigation hints
    throughout the assessment process.
    """

    AUDIOCODES = "AudioCodes"
    OTHER = "Other"


class AuditAnswer(str, Enum):
    """
    Possible assessment outcomes recorded by the assessor.

    COMPLIANT:
        The control is implemented as expected.

    NON_COMPLIANT:
        The control is missing, disabled, or implemented
        incorrectly.

    NOT_APPLICABLE:
        The control does not apply to the assessed
        environment.

    UNKNOWN:
        The assessor was unable to determine the status
        of the control during the review.
    """
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"


class VendorHints(BaseModel):
    """
    Vendor-specific navigation hints used to guide the assessor to the relevant 
    configuration within supported VoIP platforms.

    Hints may include:
    - Evidence collection guidance
    - Configuration locations
    - Platform-specific navigation paths

    These hints are intended to assist assessors in locating the relevant 
    settings during a review and are displayed within the assessment workflow 
    when available.
    """

    common: str | None = None

    audiocodes: str | None = None
    other: str | None = None


class ContextField(BaseModel):
    """
    Defines a contextual information field collected before
    the assessment begins.

    Context fields describe the reviewed environment,
    including platform information, deployment details,
    authentication services, and supporting infrastructure.

    Fields are loaded dynamically from context_fields.yaml.
    """

    id: str
    phase: str = "context"
    label: str
    type: str

    required: bool = True

    options: list[str] | None = None

    hints: VendorHints | None = None

    vendors: list[str] = Field(default_factory=lambda: ["all"])


class ReviewContext(BaseModel):
    """
    Stores environment information gathered during the assessment context 
    collection phase.

    This information is used within exported reports and provides the 
    background information required to describe the reviewed VoIP environment.

    A single ReviewContext exists for each assessment.
    """

    client_name: str

    voip_solution: VoIPPlatform

    platform_model: str

    deployment_type: str | None = None

    management_address: str | None = None

    device_type: str | None = None

    identity_provider: str | None = None

    sip_provider: str | None = None

    software_version: str | None = None

    context_notes: dict[str, str] = Field(default_factory=dict)


class QuestionResponse(BaseModel):
    """
    Represents the assessor's response to a single question.

    Responses are recorded regardless of whether a control
    is compliant or non-compliant and provide a complete
    audit trail of the assessment.
    """

    finding_id: str

    answer: AuditAnswer

    notes: str | None = None


class Question(BaseModel):
    """
    Represents a single audit question loaded from questions.yaml.

    Each question contains:
    - The review question presented to the assessor
    - Expected compliance state
    - Vulnerability mapping
    - Positive observation text
    - Remediation guidance
    - Vendor-specific navigation hints

    Questions are data-driven and should be maintained
    exclusively within the YAML configuration rather than
    hard-coded within the application.
    """

    finding_id: str
    finding_title: str
    theme: str
    commentary_group: str
    section: str
    remediation_id: str | None = None

    expected_answer: AuditAnswer

    question: str

    description: str
    commentary: str
    solution: str
    positive: str

    expected_value: str

    hints: VendorHints | None = None

    vendors: list[str] = Field(default_factory=lambda: ["all"])


class Finding(BaseModel):
    """
    Represents a non-compliant control identified during
    the assessment.

    Findings are created whenever a response does not match
    the expected secure configuration defined by the
    corresponding question.

    Each finding contains:
    - Finding identifier
    - Control categorisation
    - Description of the issue
    - Technical commentary
    - Recommended remediation
    """
    finding_id: str

    theme: str
    commentary_group: str

    section: str
    remediation_id: str | None = None

    title: str

    description: str
    commentary: str
    solution: str

    notes: str | None = None


class PositiveObservation(BaseModel):
    """
    Represents a successfully implemented security control.

    Positive observations are generated when a control
    meets the expected compliance requirements and help
    demonstrate security strengths alongside identified
    findings.
    """

    finding_id: str
    text: str
    notes: str | None = None


class AssessmentResults(BaseModel):
    """
    Represents the complete outcome of a VoIP security assessment.

    This model acts as the central object exchanged between
    the review engine and exporters.

    It contains:

    - Review context
    - Recorded responses
    - Findings
    - Positive observations

    Exporters should consume this model instead of directly
    accessing the review engine or raw YAML data.
    """

    context: ReviewContext

    findings: list[Finding] = Field(default_factory=list)

    positives: list[PositiveObservation] = Field(default_factory=list)

    responses: list[QuestionResponse] = Field(default_factory=list)