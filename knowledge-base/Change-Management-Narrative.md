# Change Management — Control Narrative

**Company:** Crestline Manufacturing, Inc.
**Document ID:** ITGC-CM-NAR-002
**Version:** 4.0
**Process owner:** Manager, Application Development
**Last reviewed:** February 2026
**In-scope systems:** SAP S/4HANA, OneStream, in-house manufacturing execution system (MES), supporting interfaces

## Purpose and scope
This narrative describes the controls over changes to in-scope applications and their underlying
configurations, ensuring changes are authorized, tested, approved, and migrated to production by
appropriately segregated personnel.

## Control activities

**ITGC-CM-01 — Change request and authorization (Preventive, Manual).**
All application changes (configuration, code, or transport) are logged in ServiceNow as a change
record describing the change, reason, and risk rating. No development work begins until the change
is authorized by the application owner.

**ITGC-CM-02 — Testing and approval (Preventive, Manual).**
Changes are tested in a non-production environment. Evidence of testing (test scripts and results,
or user acceptance sign-off for functional changes) is attached to the change record. The change
record is approved by the application owner and, for changes affecting financial reporting, by the
relevant business process owner prior to migration.

**ITGC-CM-03 — Segregation of duties over migration (Preventive, Semi-automated).**
Developers do not have access to migrate their own changes into production. Migration to production
is performed by a separate Basis/operations team member based on the approved change record. The
production transport tooling enforces this separation through restricted authorizations.

**ITGC-CM-04 — Emergency changes (Detective, Manual).**
Emergency changes may be expedited but require retroactive documentation, testing evidence, and
application-owner approval within two business days. Emergency changes are reviewed monthly by the
Application Development manager to confirm they were appropriate and properly closed.

## Related risks
Unauthorized or untested changes could introduce errors into financially significant processing,
or a developer with unrestricted migration rights could move unapproved code to production.

## Evidence retained
ServiceNow change records with authorizations and approvals; test evidence; monthly emergency-change
review; transport logs reconciled to approved change records.
