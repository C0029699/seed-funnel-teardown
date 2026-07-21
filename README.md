# seed-funnel-teardown
[README.md](https://github.com/user-attachments/files/30241245/README.md)
# Seed Health — Growth Funnel Teardown & Experiment Design

**Role:** Product Manager (Independent Study)
**Timeline:** 2025
**Tools:** Python · SQL · Amplitude (simulated) · Klaviyo flow mapping · Figma (wireframes referenced)

---

## Overview

End-to-end audit of Seed Health's (seed.com) acquisition and conversion funnel — from homepage entry through DS-01® product page to checkout — identifying friction points and designing a testable experiment to improve 30-day rebill rate.

---

## Problem Statement

Seed's homepage presents two competing CTAs:
- **"Take the Quiz"** → routes users through a health goal discovery flow
- **"Shop Now"** → routes users directly to the product catalog

Both paths converge into the **same generic post-purchase email sequence**, regardless of how the user entered or what health goal they expressed. This creates an audience bifurcation with no downstream personalization — members who took the quiz to address a specific need (gut health, energy, sleep) receive identical onboarding to those who browsed directly.

**Hypothesis:** A goal-segmented post-quiz activation flow would increase 30-day rebill rate by reducing early churn from members who feel the product does not match their stated need.

---

## Repository Structure

```
project1_seed_funnel_teardown/
│
├── data/
│   └── simulated_cohort_data.csv        # Simulated member cohort dataset
│
├── sql/
│   ├── baseline_metrics.sql             # Pull rebill rate, cancel rate, LTV baselines
│   ├── cohort_segmentation.sql          # Segment quiz vs. direct-shop members
│   └── experiment_results.sql           # Query experiment arm performance
│
├── analysis/
│   ├── funnel_audit.py                  # Funnel drop-off analysis
│   ├── cohort_analysis.py               # 30/60/90-day retention cohort curves
│   └── experiment_simulation.py         # A/B test simulation + power analysis
│
├── outputs/
│   ├── funnel_dropoff_chart.png
│   ├── cohort_retention_curves.png
│   └── experiment_results_summary.png
│
└── README.md
```

---

## Key Findings

| Funnel Stage | Observation |
|---|---|
| Homepage | Dual CTA splits audience with no tracking of which path drives higher LTV |
| Quiz flow | Health goal captured but not passed to post-purchase lifecycle system |
| Product page | Strong trust signals (ViaCap, clinical trials) but guarantee surfaced below fold |
| Checkout | Subscription default presented without trial option — potential barrier for first-time buyers |

---

## Experiment Design

**Test:** Goal-segmented onboarding email sequence vs. generic sequence (control)

| | Control | Variant |
|---|---|---|
| Segment | All new subscribers | Quiz completers only |
| Email flow | Generic DS-01® onboarding | Segmented by health goal (gut / energy / sleep) |
| Primary KPI | Day-30 rebill rate | Day-30 rebill rate |
| Guardrail metrics | Cancel rate, LTV day-90 | Cancel rate, LTV day-90 |
| Runtime | 2 weeks | 2 weeks |
| Statistical power | 80% | 80% |

---

## How to Run

```bash
pip install pandas matplotlib scipy numpy seaborn
python analysis/funnel_audit.py
python analysis/cohort_analysis.py
python analysis/experiment_simulation.py
```
