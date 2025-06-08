import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from dotenv import load_dotenv
import openpyxl
import os

load_dotenv('../.env')

# File paths
EXCEL_FOLDER = "../../data"
SCHEMA_CSV = "../config/schema_config.csv"
TABLE_NAME = "sales_data"
SCHEMA_NAME = "public"

# Collect all "INC Sales" sheets from Excel files
all_data = []

for file in os.listdir(EXCEL_FOLDER):
    if file.endswith('.xlsx') or file.endswith('.xls'):
        file_path = os.path.join(EXCEL_FOLDER, file)
        try:
            df = pd.read_excel(file_path, sheet_name='INC Sales', engine='openpyxl')
            df['Source_File'] = file.split('.')[0]
            all_data.append(df)
        except Exception as e:
            print(f"Failed to read {file}: {e}")

# Combine all the data
if not all_data:
    raise ValueError("No INC Sales sheets found in the specified folder.")

df = pd.concat(all_data, ignore_index=True)

# --- Light transformation ---
# Convert and rename date column
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y', errors='coerce').dt.strftime('%Y-%m-%d')
    df.rename(columns={'Date': 'report_date'}, inplace=True)

# Normalize column names
df.columns = df.columns.str.replace(' ', '_', regex=False) \
                       .str.replace('/', '_', regex=False) \
                       .str.replace('$', '', regex=False) \
                       .str.lower()

df = df.drop(columns='non-stock_description')

df['price_before_discount'] = df['price_before_discount'].fillna(df['saleval'])

df['location'] = df['location'].fillna('Unknown')

# --- Check output ---
# desktop_path = os.getenv('DESKTOP_PATH')
# path = f"{desktop_path}kr_sales_data.csv"
# df.to_csv(path, index=False)

# --- Upload to database ---
engine = create_engine(os.environ['DATABASE_URL'])

df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False, schema=SCHEMA_NAME)

print("Data uploaded successfully")