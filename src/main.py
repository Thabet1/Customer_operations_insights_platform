import pandas as pd
from extract import extract_csv
from load import create_snowflake_connection, load_dataframe_to_snowflake
from validate import (
    validate_nps_interactions,
    validate_agent_interactions,
    validate_unique_key,
    validate_required_columns,
    validate_no_missing_values,
    validate_allowed_values,
    validate_integer_range,
    validate_positive_integer,
    validate_customer_consistency,
    
)

interactions = extract_csv(
    "data/synthetic_interaction_records_2025.csv"
)

nps_surveys = extract_csv(
    "data/synthetic_nps_surveys_2025.csv"
)

advisors = extract_csv(
    "data/synthetic_advisor_reference.csv"
)

interactions["interaction_date"] = pd.to_datetime(
    interactions["interaction_date"]
)

nps_surveys["interaction_date"] = pd.to_datetime(
    nps_surveys["interaction_date"]
)



interactions_columns_valid = validate_required_columns(
    interactions,
    [
        "interaction_id",
        "customer_number",
        "customer_email",
        "interaction_date",
        "fcr_pass",
        "aht_seconds",
        "agent_email",
    ],
)

nps_columns_valid = validate_required_columns(
    nps_surveys,
    [
        "interaction_id",
        "customer_number",
        "customer_email",
        "interaction_date",
        "agent_email",
        "nps_score",
    ],
)

advisors_columns_valid = validate_required_columns(
    advisors,
    ["agent_email", "team_id", "team_name"],
)

nps_interactions_valid = validate_nps_interactions(
    nps_surveys, interactions
)

agent_interactions_valid = validate_agent_interactions(
    interactions, advisors
)

interaction_ids_valid = validate_unique_key(
    interactions, "interaction_id"
)

survey_ids_valid = validate_unique_key(
    nps_surveys, "interaction_id"
)

advisor_ids_valid = validate_unique_key(
    advisors, "agent_email"
)

interactions_complete = validate_no_missing_values(
    interactions,
    [
        "interaction_id",
        "customer_number",
        "customer_email",
        "interaction_date",
        "fcr_pass",
        "aht_seconds",
        "agent_email",
    ],
)

nps_complete = validate_no_missing_values(
    nps_surveys,
    [
        "interaction_id",
        "customer_number",
        "customer_email",
        "interaction_date",
        "agent_email",
        "nps_score",
    ],
)

advisors_complete = validate_no_missing_values(
    advisors,
    ["agent_email", "team_id", "team_name"],
)

fcr_values_valid = validate_allowed_values(
    interactions,
    "fcr_pass",
    ["yes", "no"],
)

nps_scores_valid = validate_integer_range(
    nps_surveys,
    "nps_score",
    0,
    10,
)

aht_values_valid = validate_positive_integer(
    interactions,
    "aht_seconds",
)

customer_consistency_valid = validate_customer_consistency(
    nps_surveys,
    interactions,
)

if not interactions_columns_valid:
    raise ValueError("Interaction dataset is missing required columns")

if not nps_columns_valid:
    raise ValueError("NPS dataset is missing required columns")

if not advisors_columns_valid:
    raise ValueError("Advisor dataset is missing required columns")

if not nps_interactions_valid:
    raise ValueError("NPS surveys reference unknown interactions")

if not agent_interactions_valid:
    raise ValueError("Interactions reference unknown advisors")

if not interaction_ids_valid:
    raise ValueError("Duplicate interaction IDs found")

if not survey_ids_valid:
    raise ValueError("Duplicate survey interaction IDs found")

if not advisor_ids_valid:
    raise ValueError("Duplicate advisor emails found")

if not interactions_complete:
    raise ValueError("Missing values found in interaction dataset")

if not nps_complete:
    raise ValueError("Missing values found in NPS dataset")

if not advisors_complete:
    raise ValueError("Missing values found in advisor dataset")

if not fcr_values_valid:
    raise ValueError("Invalid values found in FCR column")

if not nps_scores_valid:
    raise ValueError("NPS scores must be integers between 0 and 10")

if not aht_values_valid:
    raise ValueError("AHT values must be positive integers")

if not customer_consistency_valid:
    raise ValueError("Customer numbers do not match between NPS and interactions")

print("All validation checks passed")

connection = create_snowflake_connection()

try:
    load_dataframe_to_snowflake(
        dataframe=interactions,
        table_name="INTERACTIONS",
        connection=connection
    )
    
    load_dataframe_to_snowflake(
        dataframe=nps_surveys,
        table_name="NPS_SURVEYS",
        connection=connection
    )

    load_dataframe_to_snowflake(
        dataframe=advisors,
        table_name="ADVISORS",
        connection=connection
    )
    
finally:
    connection.close()
