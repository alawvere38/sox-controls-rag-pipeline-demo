# Computer Operations — Control Narrative

**Company:** Crestline Manufacturing, Inc.
**Document ID:** ITGC-CO-NAR-003
**Version:** 2.5
**Process owner:** Manager, IT Operations
**Last reviewed:** January 2026
**In-scope systems:** SAP S/4HANA, OneStream, scheduling tool (Control-M), interface monitoring

## Purpose and scope
This narrative describes controls over the scheduling, execution, and monitoring of automated batch
jobs and interfaces supporting financially significant processing, including error handling.

## Control activities

**ITGC-CO-01 — Job scheduling configuration (Preventive, Semi-automated).**
Production batch jobs and interfaces are defined and scheduled in Control-M. Changes to job
schedules follow the Change Management process (ITGC-CM). Only authorized IT Operations personnel
can modify the production schedule.

**ITGC-CO-02 — Batch job monitoring (Detective, Manual).**
IT Operations monitors the daily job calendar. Failed or abnormally terminated jobs generate alerts.
Operations reviews job completion daily and investigates failures.
*Frequency:* daily.

**ITGC-CO-03 — Job failure resolution (Detective, Manual).**
Failed jobs are logged as incidents in ServiceNow. Operations reruns or remediates the job and
documents the resolution. Failures affecting financial data are escalated to the relevant process
owner. Incidents are not closed until completion is confirmed.

**ITGC-CO-04 — Interface reconciliation (Detective, Semi-automated).**
Key interfaces (e.g., MES-to-ERP production postings, ERP-to-OneStream balances) produce
record-count and control-total reconciliations. Discrepancies are investigated and resolved before
the period is considered complete.

## Related risks
Failed or incomplete batch processing could result in incomplete or inaccurate financial data, and
undetected interface failures could cause transactions to be omitted from the general ledger.

## Evidence retained
Control-M schedule definitions; daily monitoring logs; ServiceNow incident records for failures;
interface reconciliation reports with sign-off.
