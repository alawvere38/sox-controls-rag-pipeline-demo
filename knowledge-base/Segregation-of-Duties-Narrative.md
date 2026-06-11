# Segregation of Duties and Privileged Access — Control Narrative

**Company:** Crestline Manufacturing, Inc.
**Document ID:** ITGC-SOD-NAR-005
**Version:** 1.8
**Process owner:** Director, IT Security
**Last reviewed:** February 2026
**In-scope systems:** SAP S/4HANA, OneStream, Entra ID / Active Directory

## Purpose and scope
This narrative describes controls ensuring incompatible duties are appropriately segregated and that
privileged (administrative) access is restricted and monitored.

## Control activities

**ITGC-SOD-01 — Segregation of duties ruleset (Preventive/Detective, Semi-automated).**
A defined SoD ruleset identifies conflicting access combinations (e.g., create vendor and pay
vendor; create and migrate code; post and approve journal entries). Access requests are evaluated
against the ruleset, and conflicts are flagged for review before access is granted.

**ITGC-SOD-02 — SoD conflict review and mitigation (Detective, Manual).**
On a quarterly basis, IT Security and process owners review identified SoD conflicts. Conflicts that
cannot be removed are documented with a compensating control (e.g., independent review of activity)
and approved by the process owner.
*Frequency:* quarterly.

**ITGC-SOD-03 — Privileged access restriction (Preventive, Manual).**
Administrative and superuser access (e.g., SAP_ALL, OneStream administrator, domain admin) is
limited to a minimal number of named individuals. Privileged access is requested and approved
through the standard access process with additional approval from the IT Security director.

**ITGC-SOD-04 — Privileged activity monitoring (Detective, Semi-automated).**
Activity performed under privileged accounts on in-scope systems is logged. IT Security reviews
privileged activity logs monthly for inappropriate or unexplained actions.
*Frequency:* monthly.

## Related risks
A single individual with incompatible access could initiate and conceal an unauthorized transaction,
and excessive or unmonitored privileged access could allow undetected changes to financial data or
controls.

## Evidence retained
SoD ruleset documentation; quarterly conflict reviews with mitigations and approvals; privileged
access listings with approvals; monthly privileged activity review evidence.
