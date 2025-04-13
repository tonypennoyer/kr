import pandas as pd
from db_utils import connect_db, get_schema_from_csv
from datetime import datetime

# File paths
DATA_CSV = "data/kr_sales_24_01.csv"
SCHEMA_CSV = "config/schema_config.csv"
TABLE_NAME = "sales_data"
SCHEMA_NAME = "raw"

# Read schema definition
col_defs, col_names, col_map = get_schema_from_csv(SCHEMA_CSV)

# Load and rename CSV columns
df = pd.read_csv(DATA_CSV)
df = df.rename(columns=col_map)

# Optional: convert date column to proper format (adjust column name if needed)
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # coerce invalid dates to NaT

print(df)

# # Connect to Neon DB
# conn = connect_db()
# cur = conn.cursor()

# # Create schema if not exists
# cur.execute(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}")

# # Create table if not exists
# create_query = f"""
#     CREATE TABLE IF NOT EXISTS {SCHEMA_NAME}.{TABLE_NAME} (
#         id SERIAL PRIMARY KEY,
#         {col_defs}
#     )
# """
# cur.execute(create_query)

# # Insert rows
# insert_query = f"""
#     INSERT INTO {SCHEMA_NAME}.{TABLE_NAME} ({', '.join(col_names)})
#     VALUES ({', '.join(['%s'] * len(col_names))})
# """

# # Insert each row
# for _, row in df.iterrows():
#     values = [row[col] for col in col_names]
#     cur.execute(insert_query, values)

# conn.commit()
# cur.close()
# conn.close()

# print(f"✅ {len(df)} rows inserted into {SCHEMA_NAME}.{TABLE_NAME} in Neon.")
