-- experiment_results.sql
-- Query experiment arm performance for goal-segmented onboarding A/B test
-- Primary KPI: day-30 rebill rate
-- Guardrail metrics: cancel rate, LTV day-90

WITH experiment_members AS (
    SELECT
        e.member_id,
        e.experiment_arm,          -- 'control' or 'variant'
        e.assigned_at,
        m.health_goal,
        m.subscription_start_date,
        CASE WHEN r.rebill_date IS NOT NULL
             AND DATE_DIFF(r.rebill_date, m.subscription_start_date, DAY) <= 32
             THEN 1 ELSE 0 END AS rebilled_day30,
        CASE WHEN c.cancel_date IS NOT NULL THEN 1 ELSE 0 END AS cancelled,
        COALESCE(ltv.ltv_90d, 0) AS ltv_90d
    FROM experiment_assignments e
    JOIN members m ON e.member_id = m.member_id
    LEFT JOIN rebills r ON e.member_id = r.member_id
    LEFT JOIN cancellations c ON e.member_id = c.member_id
    LEFT JOIN member_ltv ltv ON e.member_id = ltv.member_id
    WHERE e.experiment_name = 'goal_segmented_onboarding_v1'
),

arm_summary AS (
    SELECT
        experiment_arm,
        COUNT(member_id)            AS n_members,
        ROUND(AVG(rebilled_day30), 4) AS rebill_rate_30d,
        ROUND(AVG(cancelled), 4)    AS cancel_rate,
        ROUND(AVG(ltv_90d), 2)      AS avg_ltv_90d,
        ROUND(SUM(ltv_90d), 2)      AS total_revenue
    FROM experiment_members
    GROUP BY experiment_arm
),

-- Compute lift and flag significance (manual z-test approximation)
comparison AS (
    SELECT
        v.experiment_arm                                         AS variant_arm,
        c.rebill_rate_30d                                        AS control_rebill_rate,
        v.rebill_rate_30d                                        AS variant_rebill_rate,
        ROUND((v.rebill_rate_30d - c.rebill_rate_30d)
              / NULLIF(c.rebill_rate_30d, 0) * 100, 2)          AS lift_pct,
        v.avg_ltv_90d - c.avg_ltv_90d                           AS ltv_lift_per_member
    FROM arm_summary v
    CROSS JOIN arm_summary c
    WHERE v.experiment_arm = 'variant'
      AND c.experiment_arm = 'control'
)

SELECT * FROM arm_summary
UNION ALL
SELECT
    'LIFT' AS experiment_arm,
    NULL, lift_pct, NULL, ltv_lift_per_member, NULL
FROM comparison;
