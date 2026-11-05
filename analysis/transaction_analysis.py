import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote_plus


load_dotenv()

db_password = quote_plus(os.getenv("DB_PASSWORD", ""))

engine = create_engine(
    f"mysql+pymysql://"
    f"{os.getenv('DB_USER')}:{db_password}"
    f"@{os.getenv('DB_HOST', 'localhost')}:"
    f"{os.getenv('DB_PORT', '3306')}/"
    f"{os.getenv('DB_NAME')}"
)


query = """
SELECT
    transaction_id,
    account_id,
    transaction_datetime,
    amount,
    transaction_type,
    channel,
    region
FROM transactions
ORDER BY transaction_datetime;
"""

df = pd.read_sql(query, engine)

print("\nTransaction Data:")
print(df)

print("\nTotal Transactions:", len(df))
print("Total Transaction Amount:", df["amount"].sum())
print("Average Transaction Amount:", df["amount"].mean())

import numpy as np

mean_amount = df["amount"].mean()
std_amount = df["amount"].std()

statistical_threshold = mean_amount + (2 * std_amount)

print("\nNumPy Statistical Analysis:")
print("Mean Amount:", mean_amount)
print("Standard Deviation:", std_amount)
print("Statistical Threshold:", statistical_threshold)

high_value_transactions = df[
    df["amount"] > statistical_threshold
]

print("\nStatistically Unusual Transactions:")
print(
    high_value_transactions[
        ["transaction_id", "account_id", "amount", "region"]
    ]
)