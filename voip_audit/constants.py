"""
Reporting and categorisation constants.
"""

#-------------------------------------------------------------------------------
# EXECUTIVE SUMMARY
#-------------------------------------------------------------------------------

THEMES = [
    "Platform Configuration",
    "Authentication",
    "Cryptography",
    "Access Control",
    "Administrative Security",
    "Monitoring and Detection",
]


THEME_DISPLAY = {
    "Platform Configuration":
        "platform configuration and lifecycle management",

    "Authentication":
        "authentication controls",

    "Cryptography":
        "cryptographic protections",

    "Access Control":
        "administrative access control",

    "Administrative Security":
        "administrative security",

    "Monitoring and Detection":
        "logging and monitoring",
}


#-------------------------------------------------------------------------------
# COMMENTARY
#-------------------------------------------------------------------------------

COMMENTARY_ORDER = [
    "Platform Configuration and Lifecycle Management",
    "Authentication and Identity",
    "Cryptography and Communications Security",
    "Administrative Interface Security",
    "Administrative Access Control",
    "Logging and Monitoring",
]


COMMENTARY_SUMMARIES = {
    "Platform Configuration and Lifecycle Management": (
        "Several observations were identified relating to the "
        "management, maintenance, and lifecycle of the VoIP platform."
    ),

    "Authentication and Identity": (
        "Opportunities for improvement were identified within the "
        "authentication and identity controls used to protect "
        "administrative access to the VoIP environment."
    ),

    "Cryptography and Communications Security": (
        "The review identified weaknesses relating to the protection "
        "of VoIP communications and the cryptographic controls used "
        "to secure management and signalling traffic."
    ),

    "Administrative Interface Security": (
        "Several observations related to the security of administrative "
        "interfaces and the controls used to protect privileged "
        "management functions."
    ),

    "Administrative Access Control": (
        "Opportunities for improvement were identified within the "
        "controls used to restrict, review, and govern privileged "
        "administrative access."
    ),

    "Logging and Monitoring": (
        "The review highlighted weaknesses affecting the monitoring, "
        "logging, and detection capabilities of the assessed VoIP "
        "environment."
    ),
}


COMMENTARY_INTROS = {
    "Platform Configuration and Lifecycle Management":
        "The assessment identified that ",

    "Authentication and Identity":
        "Specific observations included that ",

    "Cryptography and Communications Security":
        "The review noted that ",

    "Administrative Interface Security":
        "Further observations identified that ",

    "Administrative Access Control":
        "The assessment observed that ",

    "Logging and Monitoring":
        "The assessment identified that ",
}


#-------------------------------------------------------------------------------
# REMEDIATION
#-------------------------------------------------------------------------------

REMEDIATIONS = {

    "identity_and_access_management": (
        "Enhance identity and access management controls by enforcing "
        "multi-factor authentication, using named administrative accounts, "
        "integrating with a centralised identity provider, and "
        "implementing formal account lifecycle management processes."
    ),

    "cryptography_and_communications": (
        "Protect administrative, signalling, and media traffic through "
        "the use of supported TLS versions, secure cryptographic "
        "algorithms, and encrypted VoIP communication protocols."
    ),

    "administrative_interface_security": (
        "Strengthen the security of administrative interfaces by "
        "enforcing HTTPS, restricting SSH access, implementing "
        "key-based authentication, and configuring appropriate "
        "session timeout controls."
    ),

    "privileged_access_governance": (
        "Refine privileged access controls through role-based "
        "access control, management network restrictions, periodic "
        "access reviews, and privileged access management practices."
    ),

    "logging_and_monitoring": (
        "Improve monitoring and detection capabilities by enabling "
        "comprehensive audit logging, retaining administrative audit "
        "records, forwarding logs to a centralised monitoring platform, "
        "and establishing formal log review procedures."
    ),

    "platform_lifecycle": (
        "Establish a platform lifecycle management process to ensure "
        "VoIP infrastructure components remain supported, receive "
        "security updates, and are upgraded before reaching end-of-life."
    ),
}


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