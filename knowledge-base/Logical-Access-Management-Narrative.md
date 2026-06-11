# Logical Access Management — Control Narrative

**Company:** Crestline Manufacturing, Inc.
**Document ID:** ITGC-AC-NAR-001
**Version:** 3.2
**Process owner:** Director, IT Security
**Last reviewed:** January 2026
**In-scope systems:** SAP S/4HANA (ERP), OneStream (financial consolidation), Microsoft Entra ID / Active Directory (identity provider), ServiceNow (ticketing)

## Purpose and scope
This narrative describes the controls governing how logical access to financially significant
systems is requested, approved, granted, modified, and removed at Crestline Manufacturing. It
covers all employees, contractors, and service accounts with access to in-scope systems.

## Control activities

**ITGC-AC-01 — New access provisioning (Preventive, Manual).**
All new or modified access to in-scope systems is requested through a ServiceNow access request.
The request must specify the role(s) requested and a business justification. Access is not granted
until the request is approved by (1) the requester's people manager and (2) the system/application
owner. The IT Security team provisions access only after both approvals are recorded in the ticket.
*Frequency:* per request. *Control owner:* IT Security analyst.

**ITGC-AC-02 — Terminations and transfers (Preventive/Detective, Semi-automated).**
HR initiates a termination or transfer event in Workday, which triggers an automated disable of the
user's Entra ID account within one business day for terminations. For transfers, IT Security reviews
and removes access no longer aligned to the new role within five business days.

**ITGC-AC-03 — Periodic user access review (Detective, Manual).**
On a quarterly basis, application owners review a system-generated listing of all active users and
their roles for each in-scope system, confirm continued appropriateness, and flag access for removal.
Removals identified are completed within ten business days and evidenced in ServiceNow.
*Frequency:* quarterly.

**ITGC-AC-04 — Password and authentication configuration (Preventive, Automated).**
Authentication is federated through Entra ID. Configuration enforces a minimum 14-character
password, multi-factor authentication for all users, account lockout after five failed attempts,
and 90-day rotation for non-federated service accounts. See the Information Security Policy.

## Related risks
Inappropriate or excessive access could allow unauthorized transactions or changes to financial
data, or a failure to remove access on termination could leave systems exposed to former personnel.

## Evidence retained
ServiceNow access tickets with approvals; quarterly access review packages with sign-off; Entra ID
configuration screenshots; termination feed reconciliations.
