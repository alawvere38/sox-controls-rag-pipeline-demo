# Risk and Control Matrix (RCM)

**Company:** Crestline Manufacturing, Inc.
**Document ID:** SOX-RCM-001
**Version:** 6.0
**Owner:** SOX Program Office
**Last reviewed:** February 2026

This matrix summarizes key controls supporting internal control over financial reporting (ICFR).
Full descriptions are maintained in the referenced control narratives.

## IT general controls (ITGC)

| Control ID | Control description | Type | Auto/Manual | Frequency | Owner | Source narrative |
|---|---|---|---|---|---|---|
| ITGC-AC-01 | New access requires manager + app owner approval before provisioning | Preventive | Manual | Per request | IT Security | Logical Access Management |
| ITGC-AC-03 | Quarterly user access review by application owners | Detective | Manual | Quarterly | App owners | Logical Access Management |
| ITGC-AC-04 | Authentication config (MFA, 14-char, lockout) | Preventive | Automated | Continuous | IT Security | Logical Access Management |
| ITGC-CM-01 | Changes authorized before development begins | Preventive | Manual | Per change | App Dev | Change Management |
| ITGC-CM-03 | Developers cannot migrate own changes to production | Preventive | Semi-auto | Continuous | Basis/Ops | Change Management |
| ITGC-CO-02 | Daily batch job monitoring | Detective | Manual | Daily | IT Ops | Computer Operations |
| ITGC-CO-04 | Key interface reconciliations (record counts/control totals) | Detective | Semi-auto | Per cycle | IT Ops | Computer Operations |
| ITGC-BR-03 | Annual backup restoration test | Detective | Manual | Annual | Infrastructure | Backup and Recovery |
| ITGC-SOD-02 | Quarterly SoD conflict review with mitigations | Detective | Manual | Quarterly | IT Security | Segregation of Duties |
| ITGC-SOD-04 | Monthly privileged activity log review | Detective | Semi-auto | Monthly | IT Security | Segregation of Duties |

## Business process controls

| Control ID | Control description | Type | Auto/Manual | Frequency | Owner | Source narrative |
|---|---|---|---|---|---|---|
| OTC-02 | System blocks orders over approved credit limit | Preventive | Automated | Per order | Credit Mgr | Order-to-Cash |
| OTC-03 | Monthly shipped-not-billed reconciliation | Detective | Manual | Monthly | AR | Order-to-Cash |
| OTC-05 | Monthly AR-to-GL reconciliation | Detective | Manual | Monthly | Asst Controller | Order-to-Cash |
| PTP-01 | Vendor bank-detail changes independently verified | Preventive | Manual | Per change | AP | Procure-to-Pay |
| PTP-03 | System three-way match before payment | Preventive | Automated | Per invoice | AP | Procure-to-Pay |
| PTP-05 | Payment proposal approved before release | Preventive | Manual | Per run | AP Manager | Procure-to-Pay |
| FC-01 | Journal entries require independent approval before posting | Preventive | Manual | Per entry | Accounting | Financial Close |
| FC-02 | Period-end account reconciliations independently reviewed | Detective | Manual | Monthly | Accounting | Financial Close |
| FC-05 | Controller/CFO financial statement review with variance analysis | Detective | Manual | Quarterly | Controller/CFO | Financial Close |

## Notes
Control ratings (key vs. non-key) and testing frequency are determined annually during scoping based
on materiality and risk. Compensating controls for unresolved SoD conflicts are documented in the
Segregation of Duties narrative.
