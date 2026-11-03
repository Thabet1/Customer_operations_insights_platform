SELECT
    interaction_id,
    customer_number,
    interaction_date,
    agent_email,
    team_id,
    team_name,
    fcr_pass,
    aht_seconds
FROM {{ ref('int_interactions_with_advisors') }}