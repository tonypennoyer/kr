import os
import psycopg2
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

def get_schema_from_csv(schema_config):
    schema_df = pd.read_csv(schema_csv_path)
    col_defs = ", ".join([
        f"{row['new_column']} {row['data_type']}"
        for _, row in schema_df.iterrows()
    ])
    col_map = dict(zip(schema_df['source_column'], schema_df['new_column']))
    col_names = list(schema_df['new_column'])
    return col_defs, col_names, col_map
