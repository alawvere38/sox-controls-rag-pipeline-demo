# Financial Close and Consolidation — Process Narrative

**Company:** Crestline Manufacturing, Inc.
**Document ID:** BP-FC-NAR-008
**Version:** 2.7
**Process owner:** Controller
**Last reviewed:** February 2026
**In-scope systems:** SAP S/4HANA (General Ledger), OneStream (consolidation and reporting)

## Purpose and scope
This narrative describes the period-end close, including journal entries, account reconciliations,
and consolidation, ensuring financial statements are complete, accurate, and properly reviewed.

## Process and key controls

**1. Journal entries.**
Manual journal entries are entered in SAP. *Control FC-01 (Preventive, Manual):* all manual journal
entries require preparer and independent reviewer/approver sign-off prior to posting; the preparer
cannot approve their own entry (enforced by SoD ruleset, see ITGC-SOD).

**2. Account reconciliations.**
Balance sheet accounts are reconciled at period end. *Control FC-02 (Detective, Manual):*
reconciliations are prepared and independently reviewed; reconciling items are investigated and
cleared timely. High-risk accounts are reviewed by the Assistant Controller.

**3. Data load to consolidation.**
Trial balances are loaded from SAP to OneStream via a controlled interface. *Control FC-03
(Detective, Semi-automated):* loaded balances are reconciled to the source GL via control totals
before consolidation proceeds (see ITGC-CO interface reconciliation).

**4. Consolidation and eliminations.**
OneStream performs currency translation and intercompany eliminations based on configured rules.
*Control FC-04 (Detective, Manual):* intercompany eliminations and translation results are reviewed
for reasonableness by the Consolidation Manager.

**5. Financial statement review.**
*Control FC-05 (Detective, Manual):* the Controller and CFO review consolidated results with
variance analysis against prior period and budget; significant variances are explained and
documented prior to issuance.

## Related risks
Financial statements could be misstated through unauthorized or erroneous journal entries,
unreconciled accounts, incomplete data loads, or incorrect consolidation logic.

## Evidence retained
Journal entry approvals; reconciliation packages with review sign-off; GL-to-OneStream control-total
reconciliations; elimination/translation reviews; documented financial statement review with
variance analysis.
