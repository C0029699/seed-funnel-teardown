"""
generate_data.py
Generates simulated Seed Health member cohort data for funnel analysis.
"""
import pandas as pd
import numpy as np
import os

np.random.seed(42)
N = 2000

acquisition_channel = np.random.choice(
    ['quiz', 'direct_shop', 'paid_social', 'organic_search'],
    size=N,
    p=[0.35, 0.30, 0.20, 0.15]
)

health_goal = []
for ch in acquisition_channel:
    if ch == 'quiz':
        health_goal.append(np.random.choice(['gut', 'energy', 'sleep'], p=[0.50, 0.30, 0.20]))
    else:
        health_goal.append('unknown')

rebill_30 = []
rebill_60 = []
rebill_90 = []
cancelled = []

for ch, goal in zip(acquisition_channel, health_goal):
    base = 0.72 if ch == 'quiz' else 0.65
    # quiz members with no personalization churn slightly more
    if ch == 'quiz':
        base -= 0.05
    r30 = np.random.binomial(1, base)
    r60 = np.random.binomial(1, base - 0.05) if r30 else 0
    r90 = np.random.binomial(1, base - 0.10) if r60 else 0
    cancel = 1 if not r30 else (1 if (r30 and not r60 and np.random.rand() < 0.4) else 0)
    rebill_30.append(r30)
    rebill_60.append(r60)
    rebill_90.append(r90)
    cancelled.append(cancel)

ltv_90 = []
for r30, r60, r90 in zip(rebill_30, rebill_60, rebill_90):
    ltv = 49.99 + (r30 * 49.99) + (r60 * 49.99) + (r90 * 49.99)
    ltv_90.append(round(ltv + np.random.normal(0, 3), 2))

df = pd.DataFrame({
    'member_id': [f'M{str(i).zfill(5)}' for i in range(N)],
    'acquisition_channel': acquisition_channel,
    'health_goal': health_goal,
    'rebill_day30': rebill_30,
    'rebill_day60': rebill_60,
    'rebill_day90': rebill_90,
    'cancelled': cancelled,
    'ltv_day90': ltv_90
})

os.makedirs('data', exist_ok=True)
df.to_csv('data/simulated_cohort_data.csv', index=False)
print(f"Generated {N} member records.")
print(df.groupby('acquisition_channel')[['rebill_day30', 'rebill_day60', 'rebill_day90']].mean().round(3))
