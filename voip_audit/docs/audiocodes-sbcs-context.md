### AudioCode Session Border Controllers (SBCs)

## Overview

This assessment framework is designed to support security reviews of AudioCodes Session Border Controller (SBC) deployments.

The objective of the assessment is to determine whether the AudioCodes platform has been configured and governed in a manner that aligns with organisational security requirements, vendor guidance, and recognised industry good practice. The framework guides assessors through a series of focused questions covering platform configuration, authentication, administrative security, cryptography, access control, threat protection, and monitoring capabilities. The outcome of the assessment is a set of findings and positive observations that can be used to understand the security posture of the deployment and identify opportunities for improvement.

This document serves two purposes. Firstly, it provides background information for consultants performing assessments using the tool. Secondly, it acts as a high-level introduction to AudioCodes SBC platforms for assessors who may not have prior experience reviewing SBC deployments.

## What is an SBC?

An SBC is a security and interoperability device deployed at the boundary between different voice networks. SBCs are commonly positioned between an organisation and its telecommunications provider, between unified communications platforms, or between networks with differing trust levels.

Although SBCs support call routing and protocol interoperability, they also perform a critical security function. Modern SBCs are responsible for controlling and protecting Session Initiation Protocol (SIP) signalling and Real-time Transport Protocol (RTP) media traffic. Common security capabilities include TLS encryption, Secure RTP (SRTP), topology hiding, call admission control, network segmentation, intrusion detection, protocol validation, rate limiting, and denial-of-service protection.

Because SBCs often sit at the perimeter of a communications environment and process publicly accessible traffic, they are frequently considered part of an organisation's security boundary. Weaknesses in SBC configuration may expose administrative interfaces, telephone services, authentication mechanisms, and voice communications to attack.

## What is AudioCodes?

> https://www.audiocodes.com/products/session-border-controllers-sbcs

AudioCodes is a telecommunications vendor that produces SBCs, media gateways, survivability solutions, IP phones, and voice infrastructure components. AudioCodes SBCs are widely deployed within Microsoft Teams, Cisco, Zoom Phone, and SIP trunking environments. The AudioCodes Mediant SBC range is commonly used to secure SIP communications between organisations and telecommunications providers, facilitate interoperability between voice platforms, and provide secure remote connectivity between communications environments.

AudioCodes platforms support a broad range of security functions including:

- Administrative access control
- TLS-based communications security
- Secure RTP (SRTP)
- LDAP and identity integration
- Intrusion Detection Systems (IDS)
- Malicious SIP signature detection
- Audit logging and monitoring
- Role-based administrative access

Many of these capabilities are assessed throughout this review.

## Assessment Methodology

The assessment is divided into seven areas:

1. Platform Configuration
2. Authentication
3. Administrative Security
4. Access Control
5. Cryptography and Communications Security
6. Threat Detection and Protection
7. Logging and Monitoring

Each section below provides background information intended to help assessors understand the security objectives associated with the controls being reviewed. Associated assessment controls are listed under each section for ease of reference.

### Platform Configuration

> `unsupported-software-version`

Platform Configuration focuses on how the AudioCodes platform is deployed, maintained, and supported throughout its lifecycle.

The assessment should begin by identifying the deployed software version. AudioCodes devices operate using vendor-maintained firmware that receives security updates, bug fixes, compatibility improvements, and new functionality over time. As vulnerabilities are discovered, vendors release updates to address identified weaknesses. If a platform is operating outside the vendor-supported lifecycle, it may no longer receive security updates or technical support. Because SBCs frequently process external communications and often reside within security-sensitive network locations, unsupported software may increase exposure to publicly known vulnerabilities, service disruption, fraud, interception, and unauthorised access.

The objective of this area is to determine whether the platform remains within a supported vendor lifecycle and whether software updates are managed appropriately.

### Authentication

> - `insecure-ldap-communication`
> - `admin-mfa-not-enforced`
> - `weak-password-policy`
> - `authentication-bruteforce-protection-not-configured`
> - `shared-accounts-permitted`
> - `default-accounts-insecured`

Authentication controls determine how administrators and other users prove their identity before gaining access to the platform.

Administrative access to an SBC often provides authority over signalling, routing, cryptographic controls, user administration, and network configuration. As a result, weaknesses in authentication controls can significantly increase the likelihood and impact of compromise. Many AudioCodes deployments integrate with centralised identity providers such as Active Directory, Microsoft Entra ID, LDAP, or other enterprise authentication platforms. Where external authentication services are used, the security of communications between the SBC and the authentication provider should also be reviewed. Particular attention should be paid to Multi-Factor Authentication (MFA), password policy enforcement, brute-force protection mechanisms, account ownership, and default account management.

The objective of this area is to determine whether administrative authentication is performed securely and whether sufficient controls exist to reduce the likelihood of credential compromise.

## Administrative Security

> - `http-management-enabled`
> - `insecure-cli-access-enabled`
> - `excessive-administrative-privileges`
> - `excessive-session-timeout`
> - `web-hostname-not-enforced`
> - `csrf-protection-not-enabled`
> - `ssh-key-authentication-not-used`
> - `insecure-snmp-configuration`

Administrative Security focuses on how privileged management functions are protected.

AudioCodes platforms provide multiple administrative interfaces and management protocols that may be used to configure, maintain, and monitor the platform. These interfaces often expose highly sensitive functionality capable of modifying security settings, user permissions, routing policies, and network configuration. The assessment should review the protocols used for administration, the protections applied to administrative interfaces, session management settings, role assignments, and management service hardening. Management protocols such as HTTPS, SSH, and SNMP should be configured securely and protected against unauthorised access. Additional hardening measures such as hostname enforcement, CSRF protection, and SSH key authentication may provide further protection against common attack techniques.

The objective of this area is to determine whether administrative functions are appropriately secured and accessible only to authorised users.

## Access Control

> - `insufficient-management-access-restrictions`
> - `administrative-access-not-reviewed`

Access Control focuses on restricting access to authorised users, systems, and network locations.

Administrative services should not be broadly accessible from production networks, end-user devices, or untrusted locations where alternative controls can be applied. Organisations frequently use management VLANs, dedicated management interfaces, jump hosts, firewall restrictions, network segmentation, and trusted host controls to reduce exposure of administrative services. The assessment should also evaluate whether administrative accounts remain appropriate over time. Privileged accounts that are no longer required may continue to present risk if they remain enabled and unmanaged.

The objective of this area is to determine whether access to administrative services is appropriately restricted and periodically reviewed.

## Cryptography and Communications Security
 
> - `weak-tls-configuration`
> - `weak-cryptography`
> - `signalling-and-media-encryption-not-enforced`

Cryptographic controls protect communications between administrators, managed systems, telecommunications providers, and the AudioCodes platform.

The assessment should review TLS protocol versions, cryptographic algorithms, cipher suites, key exchange settings, certificate configuration, and VoIP encryption controls. AudioCodes devices support TLS for signalling traffic and Secure RTP (SRTP) for voice communications. Without these protections, sensitive information including call metadata, authentication information, and voice conversations may be exposed to interception. The assessment should seek to determine whether communications are protected using supported protocols and whether cryptographic settings align with current vendor guidance and accepted industry practice.

The objective of this area is to determine whether communications confidentiality and integrity are protected through appropriate cryptographic controls.

## Threat Detection and Protection
 
> - `ids-not-configured`
> - `unregistered-users-permitted`

AudioCodes SBCs frequently receive communications directly from external networks and may be exposed to malicious SIP activity, automated scanning, toll fraud attempts, denial-of-service attacks, malformed protocol messages, and account compromise attempts.

To help mitigate these threats, AudioCodes platforms provide a range of detection and protection capabilities including intrusion detection, dynamic blacklisting, malicious SIP signature detection, and policy-based message validation. The assessment should determine whether these capabilities are enabled and configured appropriately. Additional attention should be given to user registration security and controls that prevent unauthorised users from placing calls through the platform.

The objective of this area is to determine whether the platform can identify, prevent, or limit malicious activity targeting VoIP services.

## Logging and Monitoring

> - `security-relevant-events-not-logged`
> - `logs-not-centrally-exported`

Logging and Monitoring controls provide visibility into activity occurring throughout the platform and support security monitoring, incident response, troubleshooting, and forensic investigation activities.

Administrative actions, authentication events, configuration changes, security alerts, and operational events should be recorded and retained appropriately. AudioCodes platforms also support Call Detail Records (CDRs), which provide additional visibility into call activity and can be valuable during investigations. The assessment should determine whether sufficient audit information is collected and whether logs are exported to a protected central monitoring platform where they can be retained, analysed, and correlated with events from other systems.

The objective of this area is to determine whether the organisation maintains sufficient visibility to detect, investigate, and respond to security-relevant activity affecting the SBC platform.