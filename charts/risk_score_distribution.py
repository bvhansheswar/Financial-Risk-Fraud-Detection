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
SELECT risk_score
FROM alerts
ORDER BY risk_score;
"""

df = pd.read_sql(query, engine)

plt.figure(figsize=(8, 5))

plt.hist(
    df["risk_score"],
    bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    edgecolor="black"
)

plt.title("Risk Score Distribution")
plt.xlabel("Risk Score")
plt.ylabel("Number of Alerts")
plt.xticks(range(0, 101, 10))

plt.tight_layout()

plt.savefig("charts/risk_score_distribution.png")

plt.show()