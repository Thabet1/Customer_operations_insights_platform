import pandas as pd
from src.validate import (
    validate_unique_key,
    validate_allowed_values,
    validate_nps_interactions,
    validate_agent_interactions,
    validate_required_columns,
    validate_integer_range,
    validate_positive_integer,
    validate_customer_consistency,
)

def test_unique_key_with_unique_values():
    dataset = pd.DataFrame({
        "interaction_id": [101, 102, 103]
    })

    result = validate_unique_key(dataset, "interaction_id")

    assert result is True


def test_unique_key_with_duplicate_values():
    dataset = pd.DataFrame({
        "interaction_id": [101, 102, 102]
    })

    result = validate_unique_key(dataset, "interaction_id")

    assert result is False
    
from src.validate import validate_no_missing_values


def test_no_missing_values():
    dataset = pd.DataFrame({
        "interaction_id": [101, 102, 103],
        "customer_number": ["C001", "C002", "C003"],
    })

    result = validate_no_missing_values(
        dataset,
        ["interaction_id", "customer_number"],
    )

    assert result is True


def test_missing_values():
    dataset = pd.DataFrame({
        "interaction_id": [101, 102, 103],
        "customer_number": ["C001", None, "C003"],
    })

    result = validate_no_missing_values(
        dataset,
        ["interaction_id", "customer_number"],
    )

    assert result is False
    
def test_allowed_values_valid():
    dataset = pd.DataFrame({
        "fcr_pass":["yes", "no"]
    })
    result = validate_allowed_values(dataset, "fcr_pass", ["yes", "no"] )

    assert result is True
    
def test_allowed_values_invalid():
    dataset = pd.DataFrame({
        "fcr_pass": ["yes", "no", "maybe"]
    })

    result = validate_allowed_values(
        dataset,
        "fcr_pass",
        ["yes", "no"]
    )

    assert result is False
    

# 1. NPS interaction references

def test_nps_interactions_valid():
    interactions = pd.DataFrame({
        "interaction_id": [101, 102, 103]
    })
    nps_surveys = pd.DataFrame({
        "interaction_id": [101, 103]
    })

    result = validate_nps_interactions(nps_surveys, interactions)

    assert result


def test_nps_interactions_invalid():
    interactions = pd.DataFrame({
        "interaction_id": [101, 102, 103]
    })
    nps_surveys = pd.DataFrame({
        "interaction_id": [101, 104]
    })

    result = validate_nps_interactions(nps_surveys, interactions)

    assert not result


# 2. Agent references

def test_agent_interactions_valid():
    interactions = pd.DataFrame({
        "agent_email": ["a@test.com", "b@test.com"]
    })
    advisors = pd.DataFrame({
        "agent_email": ["a@test.com", "b@test.com"]
    })

    result = validate_agent_interactions(interactions, advisors)

    assert result


def test_agent_interactions_invalid():
    interactions = pd.DataFrame({
        "agent_email": ["a@test.com", "unknown@test.com"]
    })
    advisors = pd.DataFrame({
        "agent_email": ["a@test.com", "b@test.com"]
    })

    result = validate_agent_interactions(interactions, advisors)

    assert not result


# 3. Required columns

def test_required_columns_valid():
    dataset = pd.DataFrame({
        "interaction_id": [101, 102],
        "customer_number": ["C001", "C002"]
    })

    result = validate_required_columns(
        dataset,
        ["interaction_id", "customer_number"]
    )

    assert result


def test_required_columns_invalid():
    dataset = pd.DataFrame({
        "interaction_id": [101, 102]
    })

    result = validate_required_columns(
        dataset,
        ["interaction_id", "customer_number"]
    )

    assert not result


# 4. Integer range

def test_integer_range_valid():
    dataset = pd.DataFrame({
        "nps_score": [0, 5, 10]
    })

    result = validate_integer_range(dataset, "nps_score", 0, 10)

    assert result


def test_integer_range_invalid():
    dataset = pd.DataFrame({
        "nps_score": [0, 5, 11]
    })

    result = validate_integer_range(dataset, "nps_score", 0, 10)

    assert not result


# 5. Positive integer

def test_positive_integer_valid():
    dataset = pd.DataFrame({
        "aht_seconds": [30, 120, 300]
    })

    result = validate_positive_integer(dataset, "aht_seconds")

    assert result


def test_positive_integer_invalid():
    dataset = pd.DataFrame({
        "aht_seconds": [30, 0, 120]
    })

    result = validate_positive_integer(dataset, "aht_seconds")

    assert not result


# 6. Customer consistency

def test_customer_consistency_valid():
    interactions = pd.DataFrame({
        "interaction_id": [101, 102],
        "customer_number": ["C001", "C002"]
    })
    nps_surveys = pd.DataFrame({
        "interaction_id": [101, 102],
        "customer_number": ["C001", "C002"]
    })

    result = validate_customer_consistency(nps_surveys, interactions)

    assert result


def test_customer_consistency_invalid():
    interactions = pd.DataFrame({
        "interaction_id": [101, 102],
        "customer_number": ["C001", "C002"]
    })
    nps_surveys = pd.DataFrame({
        "interaction_id": [101, 102],
        "customer_number": ["C001", "C999"]
    })

    result = validate_customer_consistency(nps_surveys, interactions)

    assert not result
