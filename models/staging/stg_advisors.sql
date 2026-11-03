SELECT
    agent_email,
    team_id,
    team_name
FROM {{ source('raw', 'advisors') }}