import os
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv


load_dotenv()


def create_snowflake_connection():
    connection = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
    )

    return connection


def load_dataframe_to_snowflake(dataframe, table_name, connection):
    success, chunks, rows, output = write_pandas(
        conn=connection,
        df=dataframe,
        table_name=table_name,
        database="CUSTOMER_OPERATIONS_DB",
        schema="RAW_AREA",
        auto_create_table=False,
        overwrite=False,
        quote_identifiers=False
    )

    if not success:
        raise RuntimeError(f"Failed to load data into {table_name}")

    print(f"Loaded {rows} rows into {table_name}")