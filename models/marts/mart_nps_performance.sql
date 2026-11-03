SELECT
    interaction_id,
    customer_number,
    interaction_date,
    agent_email,
    nps_score,
    CASE
        WHEN nps_score >= 9 THEN 'Promoter'
        WHEN nps_score >= 7 THEN 'Passive'
        WHEN nps_score BETWEEN 0 AND 6 THEN 'Detractor'
    END AS nps_category
FROM {{ ref('int_interactions_with_nps') }}
WHERE nps_score IS NOT NULL