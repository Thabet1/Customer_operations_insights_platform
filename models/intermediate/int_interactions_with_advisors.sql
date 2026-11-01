SELECT
    interactions.interaction_id,
    interactions.customer_number,
    interactions.customer_email,
    interactions.interaction_date,
    interactions.fcr_pass,
    interactions.aht_seconds,
    interactions.agent_email,
    advisors.team_id,
    advisors.team_name
FROM {{ ref('stg_interactions') }} AS interactions
LEFT JOIN {{ ref('stg_advisors') }} AS advisors
    ON interactions.agent_email = advisors.agent_email