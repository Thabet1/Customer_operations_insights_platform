SELECT
    interaction_id,
    customer_number,
    customer_email,
    interaction_date,
    agent_email,
    nps_score
FROM {{ source('raw', 'nps_surveys') }}