# Order-to-Cash — Process Narrative

**Company:** Crestline Manufacturing, Inc.
**Document ID:** BP-OTC-NAR-006
**Version:** 3.1
**Process owner:** Controller
**Last reviewed:** January 2026
**In-scope systems:** SAP S/4HANA (Sales & Distribution, Accounts Receivable)

## Purpose and scope
This narrative describes the order-to-cash cycle from customer order through cash application,
including the key controls over revenue recognition and accounts receivable.

## Process and key controls

**1. Customer master and credit.**
New customers and credit limits are set up in the customer master. Customer master changes require
approval; credit limits are approved by the Credit Manager. *Control OTC-01 (Preventive, Manual):*
customer master changes are reviewed against approved request forms monthly.

**2. Order entry and pricing.**
Sales orders are entered in SAP. Pricing is derived from approved price lists configured in the
system. *Control OTC-02 (Preventive, Automated):* the system blocks orders that exceed a customer's
approved credit limit until released by the Credit Manager.

**3. Shipping and revenue recognition.**
Goods are shipped from the warehouse; the goods issue posting triggers the billing process. Revenue
is recognized upon transfer of control at shipment, consistent with policy. *Control OTC-03
(Detective, Manual):* a monthly reconciliation confirms all shipments were billed (shipped-not-billed
review).

**4. Billing and invoicing.**
Invoices are generated from billing documents. *Control OTC-04 (Detective, Manual):* the AR
supervisor reviews the daily billing exception report and resolves held invoices.

**5. Cash application and AR.**
Customer payments are applied to open invoices. *Control OTC-05 (Detective, Manual):* the AR
sub-ledger is reconciled to the general ledger monthly and reviewed by the Assistant Controller.
*Control OTC-06 (Detective, Manual):* the allowance for doubtful accounts is reviewed and approved
quarterly based on an aging analysis.

## Related risks
Revenue could be recorded in the wrong period or without a valid shipment, or accounts receivable
could be misstated through unapplied cash or an inadequate allowance.

## Evidence retained
Approved customer/credit forms; shipped-not-billed reconciliation; billing exception reviews;
AR-to-GL reconciliations; quarterly allowance analysis with approval.
