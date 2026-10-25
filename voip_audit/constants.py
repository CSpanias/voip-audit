"""
Reporting and categorisation constants.
"""

# Contextual Information
INITIAL_CONTEXT_FIELDS = {
    "client_name",
    "voip_solution",
}


# Grouped Findings
THEMES = [
    "Platform Configuration",
    "Authentication",
    "Cryptography",
    "Access Control",
    "Administrative Security",
    "Monitoring and Detection",
]


# Executive Summary Stock Text
COMMENTARIES = {

    "Authentication": (
        "Weaknesses affecting authentication controls were observed, "
        "reducing assurance that administrative access is restricted "
        "to authorised users."
    ),

    "Cryptography": (
        "Several opportunities existed to strengthen the "
        "cryptographic controls protecting administrative and "
        "VoIP communications."
    ),

    "Access Control": (
        "Access control measures could be further refined to align "
        "administrative permissions with business requirements and "
        "least-privilege principles."
    ),

    "Monitoring and Detection": (
        "Logging and monitoring capabilities could be enhanced to "
        "improve visibility of security-relevant activity within "
        "the VoIP environment."
    ),

    "Administrative Security": (
        "Opportunities were noted to strengthen the governance of "
        "privileged access and administrative functions."
    ),

    "Platform Configuration": (
        "Platform configuration and lifecycle management practices "
        "could be improved to further strengthen the resilience of "
        "the VoIP environment."
    ),
}


GROUP_INTROS = {

    "Authentication":
        "Weaknesses were noted in the controls used to verify the "
        "identity of administrators and other authorised users:",

    "Cryptography":
        "Several cryptographic weaknesses were identified that may "
        "reduce the confidentiality and integrity of administrative "
        "and VoIP communications:",

    "Access Control":
        "The assessment highlighted opportunities to strengthen the "
        "controls used to govern access to administrative functions "
        "and management interfaces:",

    "Monitoring and Detection":
        "Visibility of security-relevant activity could be improved "
        "through enhanced logging, monitoring, and audit capabilities:",

    "Administrative Security":
        "Several observations related to the protection of "
        "administrative interfaces and privileged access:",

    "Platform Configuration":
        "The review found opportunities to improve the configuration "
        "and maintenance of the VoIP platform and supporting "
        "infrastructure:",
}


# References Used in the Remediation Section
REFERENCES = {
    "Generic": {
        "NCSC Secure Voice and Collaboration Services Guidance":
            "https://www.ncsc.gov.uk/",
        "NIST Cybersecurity Framework":
            "https://www.nist.gov/cyberframework",
    },

    "AudioCodes SBC": {
        "AudioCodes SBC Documentation":
            "https://techdocs.audiocodes.com/",
    },

    "AudioCodes Gateway": {
        "AudioCodes Gateway Documentation":
            "https://techdocs.audiocodes.com/",
    },
}