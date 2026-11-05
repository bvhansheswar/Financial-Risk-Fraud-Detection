from datetime import timedelta

from app import db
from app.models import Transaction


from config import (
    AMOUNT_WEIGHT,
    FREQUENCY_WEIGHT,
    LOCATION_WEIGHT,
    HIGH_AMOUNT_THRESHOLD,
    FREQUENCY_LIMIT,
    FREQUENCY_WINDOW_MINUTES
)

def calculate_risk(transaction):
    """
    Calculate an explainable risk score for a transaction.

    This system does NOT confirm fraud.
    It only flags transactions for manual review.
    """

    risk_score = 0
    reasons = []

    # -------------------------------------------------
    # Rule 1: Unusual transaction amount
    # -------------------------------------------------
    if transaction.amount > HIGH_AMOUNT_THRESHOLD:
        risk_score += AMOUNT_WEIGHT
        reasons.append(
            f"Transaction amount exceeds {HIGH_AMOUNT_THRESHOLD}"
        )

    # -------------------------------------------------
    # Rule 2: High transaction frequency
    # -------------------------------------------------
    start_time = (
        transaction.transaction_datetime
        - timedelta(minutes=FREQUENCY_WINDOW_MINUTES)
    )

    recent_transactions = Transaction.query.filter(
        Transaction.account_id == transaction.account_id,
        Transaction.transaction_datetime >= start_time,
        Transaction.transaction_datetime <= transaction.transaction_datetime,
        Transaction.transaction_id != transaction.transaction_id
    ).count()

    if recent_transactions >= FREQUENCY_LIMIT - 1:
        risk_score += FREQUENCY_WEIGHT
        reasons.append(
            f"High transaction frequency within "
            f"{FREQUENCY_WINDOW_MINUTES} minutes"
        )

    # -------------------------------------------------
    # Rule 3: Location change
    # -------------------------------------------------
    previous_transaction = (
        Transaction.query
        .filter(
            Transaction.account_id == transaction.account_id,
            Transaction.transaction_datetime < transaction.transaction_datetime
        )
        .order_by(Transaction.transaction_datetime.desc())
        .first()
    )

    if (
        previous_transaction
        and transaction.region
        and previous_transaction.region
        and transaction.region != previous_transaction.region
    ):
        risk_score += LOCATION_WEIGHT
        reasons.append(
            f"Location changed from "
            f"{previous_transaction.region} to {transaction.region}"
        )

    # -------------------------------------------------
    # Final decision
    # -------------------------------------------------
    if risk_score > 0:
        review_status = "Pending"
        reason = "; ".join(reasons)
    else:
        review_status = "Not Flagged"
        reason = "No anomaly rules triggered"

    return {
        "risk_score": risk_score,
        "review_status": review_status,
        "reason": reason
    }