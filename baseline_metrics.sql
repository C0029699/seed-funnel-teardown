-- baseline_metrics.sql
-- Pull key business metrics to establish pre-experiment baselines
-- Compatible with: BigQuery / Snowflake / Redshift (standard SQL)

WITH member_base AS (
    SELECT
        member_id,
        acquisition_channel,
        health_goal,
        subscription_start_date,
        first_rebill_date,
        cancel_date,
        ltv_90d
    FROM members
    WHERE subscription_start_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
),

rebill_flags AS (
    SELECT
        member_id,
        acquisition_channel,
        health_goal,
        CASE WHEN first_rebill_date IS NOT NULL
             AND DATE_DIFF(first_rebill_date, subscription_start_date, DAY) <= 30
             THEN 1 ELSE 0 END AS rebilled_day30,
        CASE WHEN cancel_date IS NOT NULL THEN 1 ELSE 0 END AS cancelled,
        ltv_90d
    FROM member_base
)

SELECT
    acquisition_channel,
    health_goal,
    COUNT(member_id)                        AS total_members,
    ROUND(AVG(rebilled_day30), 3)           AS rebill_rate_30d,
    ROUND(AVG(cancelled), 3)                AS cancel_rate,
    ROUND(AVG(ltv_90d), 2)                  AS avg_ltv_90d,
    ROUND(SUM(ltv_90d), 2)                  AS total_revenue_90d
FROM rebill_flags
GROUP BY 1, 2
ORDER BY acquisition_channel, rebill_rate_30d DESC;
