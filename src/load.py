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

    staging_table = f"{table_name}_STAGING"

    cursor = connection.cursor()

    try:
        cursor.execute(f"""
            CREATE TEMPORARY TABLE {staging_table}
            LIKE CUSTOMER_OPERATIONS_DB.RAW_AREA.{table_name}
        """)

        success, chunks, rows, output = write_pandas(
            conn=connection,
            df=dataframe,
            table_name=staging_table,
            database="CUSTOMER_OPERATIONS_DB",
            schema="RAW_AREA",
            auto_create_table=False,
            overwrite=False,
            quote_identifiers=False
        )

        if not success or rows != len(dataframe):
            raise RuntimeError(
                f"Failed to load all rows into {staging_table}"
            )

        cursor.execute("BEGIN")

        cursor.execute(f"""
            DELETE FROM CUSTOMER_OPERATIONS_DB.RAW_AREA.{table_name}
        """)

        cursor.execute(f"""
            INSERT INTO CUSTOMER_OPERATIONS_DB.RAW_AREA.{table_name}
            SELECT * FROM CUSTOMER_OPERATIONS_DB.RAW_AREA.{staging_table}
        """)

        connection.commit()

        print(f"Successfully replaced {table_name} with {rows} rows")

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.execute(f"DROP TABLE IF EXISTS {staging_table}")
        cursor.close()