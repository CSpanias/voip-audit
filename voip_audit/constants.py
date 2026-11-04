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

    "default-accounts-insecured":
        "default accounts secured with default credentials",

    "insecure-ldap-communication":
        "unencrypted LDAP communication",

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

    "insecure-snmp-configuration":
        "the use of insecure SNMP configuration settings",

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

    "unregistered-users-permitted":
        "calls from unregistered users",

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

    "insecure-ldap-communication":
        "LDAP communications protected using TLS",


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

    "insecure-snmp-configuration":
        "secure SNMP authentication and access controls",


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

    "unregistered-users-permitted":
        "registration-based call access controls",


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