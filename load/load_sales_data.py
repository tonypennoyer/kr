import pandas as pd
from datetime import datetime
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('../.env')

# File paths
DATA_CSV = "../../data/kr_sales_24_01.csv"
SCHEMA_CSV = "../config/schema_config.csv"
TABLE_NAME = "sales_data"
SCHEMA_NAME = "raw"

# Load and rename CSV columns
df = pd.read_csv(DATA_CSV)

df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y').dt.strftime('%Y-%m-%d')

df.rename(columns={'Date': 'report_date'}, inplace=True)

df.columns = df.columns.str.replace(' ', '_', regex=False).str.replace('/', '_', regex=False).str.replace('$', '', regex=False).str.lower()

engine = create_engine(os.environ['DATABASE_URL'])

df.to_sql('sales_data', engine, if_exists='replace', index=False)

print("Data uploaded successfully")