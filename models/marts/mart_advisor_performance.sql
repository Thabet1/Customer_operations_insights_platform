WITH interaction_metrics AS (
    SELECT
        agent_email,
        team_id,
        team_name,
        COUNT(*) AS total_interactions,
        SUM(CASE WHEN fcr_pass THEN 1 ELSE 0 END) AS fcr_interactions,
        AVG(aht_seconds) AS average_aht_seconds
    FROM {{ ref('int_interactions_with_advisors') }}
    GROUP BY
        agent_email,
        team_id,
        team_name
),

nps_metrics AS (
    SELECT
        agent_email,
        COUNT(*) AS total_surveys,
        SUM(CASE WHEN nps_score >= 9 THEN 1 ELSE 0 END) AS promoters,
        SUM(CASE WHEN nps_score BETWEEN 0 AND 6 THEN 1 ELSE 0 END) AS detractors
    FROM {{ ref('int_interactions_with_nps') }}
    WHERE nps_score IS NOT NULL
    GROUP BY agent_email
)

SELECT
    interaction_metrics.agent_email,
    interaction_metrics.team_id,
    interaction_metrics.team_name,
    interaction_metrics.total_interactions,
    interaction_metrics.fcr_interactions,
    interaction_metrics.fcr_interactions * 100.0
        / NULLIF(interaction_metrics.total_interactions, 0) AS fcr_rate,
    interaction_metrics.average_aht_seconds,
    COALESCE(nps_metrics.total_surveys, 0) AS total_surveys,
    COALESCE(nps_metrics.promoters, 0) AS promoters,
    COALESCE(nps_metrics.detractors, 0) AS detractors,
    (nps_metrics.promoters - nps_metrics.detractors) * 100.0
        / NULLIF(nps_metrics.total_surveys, 0) AS nps
FROM interaction_metrics
LEFT JOIN nps_metrics
    ON interaction_metrics.agent_email = nps_metrics.agent_email