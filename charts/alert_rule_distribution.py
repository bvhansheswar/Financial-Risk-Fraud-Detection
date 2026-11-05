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
    transaction_id,
    risk_score,
    reason
FROM alerts
WHERE alert_id >= 16
ORDER BY alert_id;
"""

df = pd.read_sql(query, engine)


# Count each actual rule from the alert reason
rule_counts = {
    "Unusual Amount": df["reason"].str.contains(
        "amount", case=False, na=False
    ).sum(),

    "High Frequency": df["reason"].str.contains(
        "frequency", case=False, na=False
    ).sum(),

    "Location Change": df["reason"].str.contains(
        "Location changed", case=False, na=False
    ).sum()
}


rule_df = pd.DataFrame(
    list(rule_counts.items()),
    columns=["rule_name", "alert_count"]
)


print("\nCurrent Rule-Based Alert Analysis:")
print(rule_df)


plt.figure(figsize=(8, 5))

plt.bar(
    rule_df["rule_name"],
    rule_df["alert_count"]
)

plt.title("Current Rule-Based Alert Distribution")
plt.xlabel("Risk Rule")
plt.ylabel("Number of Alerts")

plt.tight_layout()

plt.savefig("charts/alert_rule_distribution.png")

plt.show()