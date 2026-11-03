SELECT
    interaction_id,
    customer_number,
    customer_email,
    interaction_date,
    CASE
        WHEN UPPER(TRIM(fcr_pass)) = 'YES' THEN TRUE
        WHEN UPPER(TRIM(fcr_pass)) = 'NO' THEN FALSE
    END AS fcr_pass,
    aht_seconds,
    agent_email
FROM {{ source('raw', 'interactions') }}