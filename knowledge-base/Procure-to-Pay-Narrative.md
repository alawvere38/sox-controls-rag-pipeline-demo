# Procure-to-Pay — Process Narrative

**Company:** Crestline Manufacturing, Inc.
**Document ID:** BP-PTP-NAR-007
**Version:** 3.0
**Process owner:** Controller
**Last reviewed:** January 2026
**In-scope systems:** SAP S/4HANA (Materials Management, Accounts Payable)

## Purpose and scope
This narrative describes the procure-to-pay cycle from requisition through vendor payment, including
key controls over purchasing, receiving, and accounts payable.

## Process and key controls

**1. Vendor master.**
New vendors and vendor bank-detail changes are set up in the vendor master. *Control PTP-01
(Preventive, Manual):* vendor master additions and bank-detail changes require independent
verification and approval before activation, and are reviewed monthly against supporting requests.

**2. Requisition and purchase order.**
Purchase requisitions are entered and converted to purchase orders. *Control PTP-02 (Preventive,
Semi-automated):* POs are subject to system-enforced approval thresholds based on amount; approvals
route to the appropriate level of management.

**3. Receiving.**
Goods receipts are recorded upon delivery. *Control PTP-03 (Preventive, Automated):* the system
performs a three-way match of purchase order, goods receipt, and invoice before an invoice is
released for payment; mismatches are blocked.

**4. Invoice processing.**
Vendor invoices are entered or received electronically and matched. *Control PTP-04 (Detective,
Manual):* the AP supervisor reviews and clears the blocked-invoice and price-variance reports weekly.

**5. Payment.**
Approved invoices are paid through the payment run. *Control PTP-05 (Preventive, Manual):* the
payment proposal is reviewed and approved by the AP Manager before release. *Control PTP-06
(Detective, Manual):* the AP sub-ledger is reconciled to the general ledger monthly and reviewed by
the Assistant Controller.

## Related risks
Payments could be made to fictitious or incorrect vendors, goods/services could be paid for without
receipt, or accounts payable could be misstated.

## Evidence retained
Approved vendor request forms with verification; PO approval evidence; three-way match
configuration; weekly blocked-invoice reviews; approved payment proposals; AP-to-GL reconciliations.
