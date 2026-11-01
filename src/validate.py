def validate_nps_interactions(nps_surveys, interactions):
    results = nps_surveys["interaction_id"].isin(
        interactions["interaction_id"]
    ).all()
    return results


def validate_agent_interactions(interactions, advisors):
    results = interactions["agent_email"].isin(
        advisors["agent_email"]
    ).all()
    return results

def validate_unique_key(dataset, key_column):
    return dataset[key_column].is_unique

def validate_required_columns(dataset, required_columns):
    return set(required_columns).issubset(dataset.columns)

def validate_no_missing_values(dataset, required_columns):
    return not dataset[required_columns].isna().any().any()

def validate_allowed_values(dataset, column, allowed_values):
    return bool(dataset[column].isin(allowed_values).all())

def validate_integer_range(dataset, column, minimum, maximum):
    values = dataset[column]

    return (
        values.mod(1).eq(0).all()
        and values.between(minimum, maximum).all()
    )

def validate_positive_integer(dataset, column):
    values = dataset[column]

    return (
        values.mod(1).eq(0).all()
        and values.gt(0).all()
    )
    
def validate_customer_consistency(nps_surveys, interactions):
    interaction_customers = interactions.set_index(
        "interaction_id"
    )["customer_number"]

    expected_customers = nps_surveys["interaction_id"].map(
        interaction_customers
    )

    return expected_customers.eq(
        nps_surveys["customer_number"]
    ).all()