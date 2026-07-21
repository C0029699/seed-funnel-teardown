"""
experiment_simulation.py
Simulates the A/B test: Generic onboarding (control) vs.
Goal-segmented onboarding (variant) for quiz completers.
Outputs: experiment_results_summary.png + statistical test results
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import os

os.makedirs('outputs', exist_ok=True)
np.random.seed(99)

# --- Parameters ---
N_PER_ARM = 500
CONTROL_REBILL_RATE = 0.65     # baseline: generic onboarding
VARIANT_REBILL_RATE = 0.73     # hypothesis: +8pp lift from personalization
ALPHA = 0.05
POWER = 0.80

# --- Simulate experiment arms ---
control = np.random.binomial(1, CONTROL_REBILL_RATE, N_PER_ARM)
variant = np.random.binomial(1, VARIANT_REBILL_RATE, N_PER_ARM)

# --- Statistical test (two-proportion z-test) ---
p_control = control.mean()
p_variant = variant.mean()
p_pool = (control.sum() + variant.sum()) / (N_PER_ARM * 2)
se = np.sqrt(p_pool * (1 - p_pool) * (2 / N_PER_ARM))
z_stat = (p_variant - p_control) / se
p_value = 1 - stats.norm.cdf(z_stat)
lift = (p_variant - p_control) / p_control * 100

print("=" * 50)
print("EXPERIMENT RESULTS: Goal-Segmented Onboarding")
print("=" * 50)
print(f"Control rebill rate:  {p_control:.1%} (n={N_PER_ARM})")
print(f"Variant rebill rate:  {p_variant:.1%} (n={N_PER_ARM})")
print(f"Lift:                 {lift:+.1f}%")
print(f"Z-statistic:          {z_stat:.2f}")
print(f"P-value:              {p_value:.4f}")
print(f"Significant (α=0.05): {'✅ YES' if p_value < ALPHA else '❌ NO'}")
print("=" * 50)

# --- LTV impact simulation ---
avg_monthly_rev = 49.99
control_ltv_3mo = p_control * avg_monthly_rev * 3
variant_ltv_3mo = p_variant * avg_monthly_rev * 3
ltv_lift_per_member = variant_ltv_3mo - control_ltv_3mo
print(f"\nEstimated LTV lift per member (3-month): ${ltv_lift_per_member:.2f}")
print(f"Projected impact on 10,000 members/mo:  ${ltv_lift_per_member * 10000:,.0f}")

# --- Visualization ---
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Chart 1: Rebill Rate Comparison
ax1 = axes[0]
bars = ax1.bar(['Control\n(Generic)', 'Variant\n(Goal-Segmented)'],
               [p_control, p_variant],
               color=['#97BC62', '#2C5F2E'], width=0.45, edgecolor='white')
ax1.set_ylim(0, 1)
ax1.set_ylabel('Day-30 Rebill Rate')
ax1.set_title('A/B Test: Day-30 Rebill Rate\nControl vs. Variant', fontweight='bold')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
for bar, val in zip(bars, [p_control, p_variant]):
    ax1.text(bar.get_x() + bar.get_width() / 2, val + 0.01,
             f'{val:.1%}', ha='center', fontsize=12, fontweight='bold')
sig_text = f'p = {p_value:.3f} {"✓ Significant" if p_value < ALPHA else "✗ Not significant"}'
ax1.text(0.5, 0.92, sig_text, transform=ax1.transAxes,
         ha='center', fontsize=9, color='#2C5F2E' if p_value < ALPHA else '#c0392b',
         bbox=dict(boxstyle='round', facecolor='#f0f8f0', edgecolor='#2C5F2E', alpha=0.7))

# Chart 2: LTV Projection
ax2 = axes[1]
members = [1000, 5000, 10000, 25000]
ltv_impacts = [ltv_lift_per_member * m for m in members]
bars2 = ax2.bar([f'{m:,}' for m in members], ltv_impacts,
                color='#2C5F2E', edgecolor='white')
ax2.set_xlabel('Monthly New Quiz Subscribers')
ax2.set_ylabel('3-Month LTV Impact ($)')
ax2.set_title('Projected Revenue Impact\nGoal-Segmented Onboarding', fontweight='bold')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'${y:,.0f}'))
for bar, val in zip(bars2, ltv_impacts):
    ax2.text(bar.get_x() + bar.get_width() / 2, val + 200,
             f'${val:,.0f}', ha='center', fontsize=9, fontweight='bold')

plt.suptitle('Seed Health — Experiment: Goal-Segmented Onboarding vs. Generic',
             fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/experiment_results_summary.png', dpi=150, bbox_inches='tight')
print("\nSaved: outputs/experiment_results_summary.png")
plt.close()
