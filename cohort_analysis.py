"""
cohort_analysis.py
Plots 30/60/90-day retention curves segmented by acquisition channel and health goal.
Outputs: cohort_retention_curves.png
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs('outputs', exist_ok=True)
df = pd.read_csv('data/simulated_cohort_data.csv')

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# --- Chart 1: Retention by Acquisition Channel ---
channels = df['acquisition_channel'].unique()
days = [30, 60, 90]
colors = {'quiz': '#2C5F2E', 'direct_shop': '#97BC62',
          'paid_social': '#F4A261', 'organic_search': '#264653'}

ax1 = axes[0]
for ch in channels:
    sub = df[df['acquisition_channel'] == ch]
    rates = [
        sub['rebill_day30'].mean(),
        sub['rebill_day60'].mean(),
        sub['rebill_day90'].mean()
    ]
    ax1.plot(days, rates, marker='o', label=ch.replace('_', ' ').title(),
             color=colors.get(ch, '#999'), linewidth=2)

ax1.set_title('Retention by Acquisition Channel', fontsize=12, fontweight='bold')
ax1.set_xlabel('Day')
ax1.set_ylabel('Rebill Rate')
ax1.set_xticks(days)
ax1.set_ylim(0, 1)
ax1.legend(fontsize=9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
ax1.axvline(x=30, color='gray', linestyle='--', alpha=0.3)
ax1.text(30.5, 0.95, 'Key rebill\nwindow', fontsize=8, color='gray')

# --- Chart 2: Quiz Members — Retention by Health Goal ---
ax2 = axes[1]
quiz_df = df[df['acquisition_channel'] == 'quiz']
goal_colors = {'gut': '#2C5F2E', 'energy': '#F4A261', 'sleep': '#264653'}

for goal in ['gut', 'energy', 'sleep']:
    sub = quiz_df[quiz_df['health_goal'] == goal]
    rates = [
        sub['rebill_day30'].mean(),
        sub['rebill_day60'].mean(),
        sub['rebill_day90'].mean()
    ]
    ax2.plot(days, rates, marker='o', label=f'{goal.title()} goal',
             color=goal_colors[goal], linewidth=2)

ax2.set_title('Quiz Members: Retention by Health Goal\n(No Personalization = Flat Curves)', fontsize=12, fontweight='bold')
ax2.set_xlabel('Day')
ax2.set_ylabel('Rebill Rate')
ax2.set_xticks(days)
ax2.set_ylim(0, 1)
ax2.legend(fontsize=9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))

insight = "Opportunity: goal-segmented\nonboarding could lift all curves"
ax2.text(55, 0.35, insight, fontsize=8, color='#c0392b',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='#fdecea', edgecolor='#c0392b', alpha=0.8))

plt.suptitle('Seed Health — Cohort Retention Analysis', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/cohort_retention_curves.png', dpi=150, bbox_inches='tight')
print("Saved: outputs/cohort_retention_curves.png")
plt.close()

# --- Summary Stats ---
print("\n=== LTV by Acquisition Channel ===")
print(df.groupby('acquisition_channel')['ltv_day90'].agg(['mean', 'median', 'std']).round(2).to_string())

print("\n=== Cancel Rate by Channel ===")
print(df.groupby('acquisition_channel')['cancelled'].mean().round(3).to_string())
