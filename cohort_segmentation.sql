-- cohort_segmentation.sql
-- Segment quiz completers vs. direct shop members
-- Used to identify personalization gap in post-purchase lifecycle

WITH quiz_members AS (
    SELECT
        m.member_id,
        m.acquisition_channel,
        q.health_goal,
        q.quiz_completed_at,
        m.subscription_start_date,
        CASE WHEN q.member_id IS NOT NULL THEN 1 ELSE 0 END AS took_quiz,
        CASE WHEN lc.email_sequence_type = 'goal_segmented' THEN 1 ELSE 0 END AS received_personalized_flow
    FROM members m
    LEFT JOIN quiz_responses q
        ON m.member_id = q.member_id
    LEFT JOIN lifecycle_events lc
        ON m.member_id = lc.member_id
        AND lc.event_type = 'onboarding_email_sequence'
),

segmentation_summary AS (
    SELECT
        health_goal,
        took_quiz,
        received_personalized_flow,
        COUNT(member_id)    AS members,
        -- This is the key gap: quiz takers who got generic flow
        SUM(CASE WHEN took_quiz = 1 AND received_personalized_flow = 0
                 THEN 1 ELSE 0 END) AS quiz_with_generic_flow
    FROM quiz_members
    GROUP BY 1, 2, 3
)

SELECT
    health_goal,
    took_quiz,
    received_personalized_flow,
    members,
    quiz_with_generic_flow,
    ROUND(quiz_with_generic_flow * 1.0 / NULLIF(members, 0), 3) AS pct_quiz_not_personalized
FROM segmentation_summary
ORDER BY health_goal, took_quiz DESC;
