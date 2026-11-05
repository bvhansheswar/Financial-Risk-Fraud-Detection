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
    alert_id,
    review_status
FROM alerts
WHERE alert_id >= 16
ORDER BY alert_id;
"""

df = pd.read_sql(query, engine)


status_counts = (
    df["review_status"]
    .value_counts()
    .reindex(
        ["Pending", "Reviewed", "Escalated"],
        fill_value=0
    )
)


print("\nCurrent Rule-Engine Alert Status:")
print(status_counts)


plt.figure(figsize=(8, 5))

plt.bar(
    status_counts.index,
    status_counts.values
)

plt.title("Current Rule-Based Alert Status Distribution")
plt.xlabel("Review Status")
plt.ylabel("Number of Alerts")

plt.tight_layout()

plt.savefig("charts/alert_status_distribution.png")

plt.show()