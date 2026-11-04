"""
Reporting and categorisation constants.
"""

#-------------------------------------------------------------------------------
# EXECUTIVE SUMMARY
#-------------------------------------------------------------------------------

TITLE_REWRITES = {
    "unsupported-software-version":
        "the use of a software version outside the preferred support stream",

    "admin-mfa-not-enforced":
        "the absence of multi-factor authentication for administrative access",

    "weak-password-policy":
        "weak password policy settings",

    "authentication-bruteforce-protection-not-configured":
        "the absence of protections against repeated authentication attempts",

    "shared-accounts-permitted":
        "the use of shared administrative accounts",

    "default-accounts-enabled":
        "the presence of default administrative accounts",

    "http-management-enabled":
        "administrative web access over HTTP",

    "insecure-cli-access-enabled":
        "the use of insecure command-line administration protocols",

    "excessive-administrative-privileges":
        "inappropriate assignment of administrative privileges",

    "excessive-session-timeout":
        "excessive administrative session duration",

    "web-hostname-not-enforced":
        "the absence of hostname enforcement for the web management interface",

    "csrf-protection-not-enabled":
        "the absence of CSRF protection for the administrative web interface",

    "ssh-key-authentication-not-used":
        "the use of password-based SSH administration",

    "insufficient-management-access-restrictions":
        "insufficient restrictions on management interface access",

    "administrative-access-not-reviewed":
        "insufficient review of privileged account access",

    "weak-tls-configuration":
        "support for legacy TLS protocol versions",

    "weak-cryptography":
        "the use of weak cryptographic algorithms",

    "signalling-and-media-encryption-not-enforced":
        "unencrypted VoIP signalling or media communications",

    "ids-not-configured":
        "the absence of intrusion detection controls",

    "security-relevant-events-not-logged":
        "insufficient logging of security-relevant events",

    "logs-not-centrally-exported":
        "the absence of centralised security log collection",
}


POSITIVE_REWRITES = {

    # Platform Configuration

    "unsupported-software-version":
        "a vendor-supported software version",


    # Authentication

    "admin-mfa-not-enforced":
        "multi-factor authentication for administrative access",

    "weak-password-policy":
        "strong password controls for administrative accounts",

    "authentication-bruteforce-protection-not-configured":
        "protections against repeated authentication attacks",

    "shared-accounts-permitted":
        "uniquely assigned administrative accounts",

    "default-accounts-insecured":
        "default accounts secured with non-default credentials",


    # Administrative Security

    "http-management-enabled":
        "HTTPS-only administrative access",

    "insecure-cli-access-enabled":
        "secure administrative CLI access",

    "excessive-administrative-privileges":
        "appropriate assignment of administrative privileges",

    "excessive-session-timeout":
        "appropriate administrative session timeout controls",

    "web-hostname-not-enforced":
        "web management hostname enforcement",

    "csrf-protection-not-enabled":
        "CSRF protection for administrative interfaces",

    "ssh-key-authentication-not-used":
        "SSH key-based administrative access",


    # Access Control

    "insufficient-management-access-restrictions":
        "restricted management network access",

    "administrative-access-not-reviewed":
        "regular review of privileged administrative accounts",


    # Cryptography

    "weak-tls-configuration":
        "supported TLS protocol versions",

    "weak-cryptography":
        "strong cryptographic algorithms and key exchange parameters",

    "signalling-and-media-encryption-not-enforced":
        "encrypted SIP signalling and voice communications",


    # Threat Protection

    "ids-not-configured":
        "intrusion detection controls for malicious SIP activity",


    # Monitoring

    "security-relevant-events-not-logged":
        "appropriate audit logging configuration",

    "logs-not-centrally-exported":
        "centralised Syslog integration",
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
    "Threat Detection and Protection",
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

    "Threat Detection and Protection": (
        "The review identified opportunities to improve the detection "
        "and prevention of malicious activity targeting the VoIP "
        "environment."
    ),

    "Logging and Monitoring": (
        "The assessment reviewed the monitoring, logging, and detection "
        "capabilities of the assessed VoIP environment."
    ),
}


THEME_REWRITES = {
    "Authentication and Identity":
        "authentication controls",

    "Cryptography and Communications Security":
        "cryptographic configuration",

    "Administrative Interface Security":
        "administrative interface security",

    "Administrative Access Control":
        "privileged access management",

    "Threat Detection and Protection":
        "threat detection capabilities",

    "Logging and Monitoring":
        "security monitoring and logging controls",

    "Platform Configuration and Lifecycle Management":
        "platform lifecycle management",
}


COMMENTARY_INTROS = {
    "Platform Configuration and Lifecycle Management":
        "The assessment identified ",

    "Authentication and Identity":
        "Review of authentication controls identified ",

    "Cryptography and Communications Security":
        "The assessment identified ",

    "Administrative Interface Security":
        "Further assessment identified ",

    "Administrative Access Control":
        "The review identified ",

    "Threat Detection and Protection":
        "The assessment identified ",

    "Logging and Monitoring":
        "The review identified ",
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
        "enforcing HTTPS, restricting management access, "
        "implementing SSH key-based authentication where "
        "appropriate, configuring hostname enforcement for web "
        "administration, and applying suitable session timeout "
        "controls."
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