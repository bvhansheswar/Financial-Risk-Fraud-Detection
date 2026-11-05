import os

import pandas as pd
import matplotlib.pyplot as plt
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
    transaction_datetime,
    amount
FROM transactions
ORDER BY transaction_datetime;
"""

df = pd.read_sql(query, engine)

df["transaction_datetime"] = pd.to_datetime(
    df["transaction_datetime"]
)


plt.figure(figsize=(10, 5))

plt.plot(
    df["transaction_datetime"],
    df["amount"],
    marker="o"
)

plt.title("Transaction Amount Trend")
plt.xlabel("Transaction Date and Time")
plt.ylabel("Transaction Amount")

plt.xticks(rotation=30)

plt.tight_layout()

plt.savefig("charts/transaction_amount_trend.png")

plt.show()