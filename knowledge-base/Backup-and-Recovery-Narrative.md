# Backup and Recovery — Control Narrative

**Company:** Crestline Manufacturing, Inc.
**Document ID:** ITGC-BR-NAR-004
**Version:** 2.1
**Process owner:** Manager, Infrastructure
**Last reviewed:** December 2025
**In-scope systems:** SAP S/4HANA database, OneStream database, supporting file shares

## Purpose and scope
This narrative describes controls ensuring that financially significant data can be backed up and
restored in the event of a processing failure or disaster.

## Control activities

**ITGC-BR-01 — Backup scheduling and execution (Preventive, Automated).**
Production databases for in-scope systems are backed up on an automated schedule: full backups
weekly and incremental backups daily. Backup jobs are configured in the enterprise backup tool and
run without manual intervention.

**ITGC-BR-02 — Backup monitoring (Detective, Manual).**
Infrastructure reviews backup completion daily. Failed backups generate alerts, are logged as
incidents, and are rerun. Backups are not considered complete until a successful run is confirmed.
*Frequency:* daily.

**ITGC-BR-03 — Restoration testing (Detective, Manual).**
A test restoration of an in-scope system backup is performed at least annually to confirm backups
are recoverable. Results are documented, and any failures are remediated and re-tested.
*Frequency:* annual.

**ITGC-BR-04 — Offsite/redundant storage (Preventive, Automated).**
Backups are replicated to a geographically separate location to support recovery in a disaster
scenario, consistent with the IT disaster recovery plan.

## Related risks
A loss of financial data without a recoverable backup could prevent accurate financial reporting,
and untested backups could prove unrecoverable when needed.

## Evidence retained
Backup tool schedule and completion logs; daily monitoring evidence; annual restoration test
documentation; replication configuration.
