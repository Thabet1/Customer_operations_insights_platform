SELECT
    interactions.interaction_id,
    interactions.customer_number,
    interactions.interaction_date,
    interactions.agent_email,
    interactions.fcr_pass,
    interactions.aht_seconds,
    surveys.nps_score
FROM {{ ref('stg_interactions') }} AS interactions
LEFT JOIN {{ ref('stg_nps_surveys') }} AS surveys
    ON interactions.interaction_id = surveys.interaction_id