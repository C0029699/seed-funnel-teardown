"""
funnel_audit.py
Analyzes Seed Health acquisition funnel drop-off by channel.
Outputs: funnel_dropoff_chart.png
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

os.makedirs('outputs', exist_ok=True)

# Load data (run generate_data.py first)
df = pd.read_csv('data/simulated_cohort_data.csv')

# --- Funnel Stage Simulation ---
# Simulate homepage visitors -> add to cart -> checkout -> subscribe -> rebill
funnel_stages = {
    'Homepage Visitors':    10000,
    'Product Page Views':   4200,
    'Add to Cart':          1800,
    'Checkout Started':     1200,
    'Subscribed':           900,
    'Day-30 Rebill':        int(900 * df['rebill_day30'].mean()),
    'Day-90 Rebill':        int(900 * df['rebill_day90'].mean()),
}

stages = list(funnel_stages.keys())
values = list(funnel_stages.values())
drop_pct = [None] + [
    round((values[i-1] - values[i]) / values[i-1] * 100, 1)
    for i in range(1, len(values))
]

fig, ax = plt.subplots(figsize=(10, 6))
colors = ['#2C5F2E' if v > 500 else '#97BC62' for v in values]

bars = ax.barh(stages[::-1], values[::-1], color=colors[::-1], height=0.55, edgecolor='white')

for i, (bar, val, drop) in enumerate(zip(bars, values[::-1], drop_pct[::-1])):
    ax.text(val + 80, bar.get_y() + bar.get_height() / 2,
            f'{val:,}', va='center', fontsize=10, fontweight='bold', color='#222')
    if drop is not None:
        ax.text(val + 80, bar.get_y() + bar.get_height() / 2 - 0.22,
                f'▼ {drop}% drop', va='center', fontsize=8, color='#c0392b')

ax.set_xlabel('Users', fontsize=11)
ax.set_title('Seed Health — Acquisition Funnel Drop-off Analysis', fontsize=13, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(0, max(values) * 1.25)

plt.tight_layout()
plt.savefig('outputs/funnel_dropoff_chart.png', dpi=150, bbox_inches='tight')
print("Saved: outputs/funnel_dropoff_chart.png")
plt.close()

# --- Channel Breakdown ---
print("\n=== Rebill Rate by Acquisition Channel ===")
summary = df.groupby('acquisition_channel').agg(
    members=('member_id', 'count'),
    rebill_30=('rebill_day30', 'mean'),
    rebill_60=('rebill_day60', 'mean'),
    rebill_90=('rebill_day90', 'mean'),
    avg_ltv=('ltv_day90', 'mean')
).round(3)
print(summary.to_string())
