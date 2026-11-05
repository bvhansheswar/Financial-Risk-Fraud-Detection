from flask import Blueprint, jsonify, request, render_template
from datetime import datetime
from app import db
from app.models import Customer, Account, Transaction, Alert, AuditLog
from app.risk_engine import calculate_risk

api = Blueprint("api", __name__)

@api.route("/dashboard", methods=["GET"])
def dashboard():
    total_transactions = Transaction.query.count()

    current_alerts = Alert.query.filter_by(
        rule_name="Rule-Based Risk"
    ).all()

    alert_count = len(current_alerts)

    alert_rate = (
        (alert_count / total_transactions) * 100
        if total_transactions > 0
        else 0
    )

    escalated_count = sum(
        1
        for alert in current_alerts
        if alert.review_status == "Escalated"
    )

    transactions = (
        Transaction.query
        .order_by(Transaction.transaction_datetime.desc())
        .limit(10)
        .all()
    )
    alerts = (
        Alert.query
        .filter_by(rule_name="Rule-Based Risk")
        .order_by(Alert.alert_id.desc())
        .all()
    )

    return render_template(
        "dashboard.html",
        total_transactions=total_transactions,
        alert_count=alert_count,
        alert_rate=alert_rate,
        escalated_count=escalated_count,
        transactions=transactions,
        alerts=alerts
    )

@api.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": "success",
        "message": "Financial Risk & Fraud Detection API is running"
    })


@api.route("/api/customers", methods=["GET"])
def get_customers():
    customers = Customer.query.all()

    return jsonify([
        {
            "customer_id": customer.customer_id,
            "customer_code": customer.customer_code
        }
        for customer in customers
    ])

@api.route("/api/accounts", methods=["GET"])
def get_accounts():
    accounts = Account.query.all()

    return jsonify([
        {
            "account_id": account.account_id,
            "customer_id": account.customer_id
        }
        for account in accounts
    ])

@api.route("/api/transactions", methods=["GET"])
def get_transactions():
    transactions = Transaction.query.all()

    return jsonify([
        {
            "transaction_id": transaction.transaction_id,
            "account_id": transaction.account_id,
            "transaction_datetime": transaction.transaction_datetime.isoformat(),
            "amount": float(transaction.amount),
            "transaction_type": transaction.transaction_type,
            "channel": transaction.channel,
            "region": transaction.region
        }
        for transaction in transactions
    ])

@api.route("/api/transactions/<int:transaction_id>/risk", methods=["GET"])
def get_transaction_risk(transaction_id):

    transaction = Transaction.query.get(transaction_id)

    if transaction is None:
        return jsonify({
            "error": "Transaction not found"
        }), 404

    risk_result = calculate_risk(transaction)

    # Store alert only when an anomaly is detected
    if risk_result["risk_score"] > 0:

        existing_alert = Alert.query.filter_by(
            transaction_id=transaction.transaction_id,
            rule_name="Rule-Based Risk"
        ).first()

        if existing_alert:
            existing_alert.risk_score = risk_result["risk_score"]
            existing_alert.reason = risk_result["reason"]
            existing_alert.review_status = risk_result["review_status"]

        else:
            new_alert = Alert(
                transaction_id=transaction.transaction_id,
                rule_name="Rule-Based Risk",
                risk_score=risk_result["risk_score"],
                reason=risk_result["reason"],
                review_status=risk_result["review_status"]
            )

            db.session.add(new_alert)

        db.session.commit()

    return jsonify({
        "transaction_id": transaction.transaction_id,
        "risk_score": risk_result["risk_score"],
        "review_status": risk_result["review_status"],
        "reason": risk_result["reason"]
    })

@api.route("/api/transactions", methods=["POST"])
def create_transaction():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    # Required fields
    required_fields = [
        "account_id",
        "transaction_datetime",
        "amount",
        "transaction_type",
        "channel"
    ]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    # Validate account
    account = Account.query.get(data["account_id"])

    if account is None:
        return jsonify({
            "error": "Account not found"
        }), 404

    # Validate amount
    try:
        amount = float(data["amount"])
    except (TypeError, ValueError):
        return jsonify({
            "error": "Amount must be a valid number"
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "Amount must be greater than 0"
        }), 400

    # Validate datetime
    try:
        transaction_datetime = datetime.fromisoformat(
            data["transaction_datetime"]
        )
    except (TypeError, ValueError):
        return jsonify({
            "error": "Invalid datetime format. Use YYYY-MM-DDTHH:MM:SS"
        }), 400

    # Create transaction
    new_transaction = Transaction(
        account_id=data["account_id"],
        transaction_datetime=transaction_datetime,
        amount=amount,
        transaction_type=data["transaction_type"],
        channel=data["channel"],
        region=data.get("region")
    )

    db.session.add(new_transaction)
    db.session.commit()

    # Calculate risk
    risk_result = calculate_risk(new_transaction)

    # Create alert if anomaly detected
    if risk_result["risk_score"] > 0:

        new_alert = Alert(
            transaction_id=new_transaction.transaction_id,
            rule_name="Rule-Based Risk",
            risk_score=risk_result["risk_score"],
            reason=risk_result["reason"],
            review_status=risk_result["review_status"]
        )

        db.session.add(new_alert)
        db.session.commit()

    return jsonify({
        "message": "Transaction created successfully",
        "transaction_id": new_transaction.transaction_id,
        "account_id": new_transaction.account_id,
        "amount": float(new_transaction.amount),
        "risk_score": risk_result["risk_score"],
        "review_status": risk_result["review_status"],
        "reason": risk_result["reason"]
    }), 201

@api.route("/api/alerts", methods=["GET"])
def get_alerts():

    alerts = Alert.query.order_by(
        Alert.alert_id.desc()
    ).all()

    return jsonify([
        {
            "alert_id": alert.alert_id,
            "transaction_id": alert.transaction_id,
            "rule_name": alert.rule_name,
            "risk_score": alert.risk_score,
            "reason": alert.reason,
            "review_status": alert.review_status
        }
        for alert in alerts
    ])

@api.route("/api/alerts/<int:alert_id>/status", methods=["PUT"])
def update_alert_status(alert_id):

    alert = Alert.query.get(alert_id)

    if alert is None:
        return jsonify({
            "error": "Alert not found"
        }), 404

    data = request.get_json(silent=True)

    if not data or "review_status" not in data:
        return jsonify({
            "error": "review_status is required"
        }), 400

    allowed_statuses = [
        "Pending",
        "Reviewed",
        "Escalated"
    ]

    if data["review_status"] not in allowed_statuses:
        return jsonify({
            "error": "Invalid review status",
            "allowed_statuses": allowed_statuses
        }), 400

    alert.review_status = data["review_status"]

    audit_log = AuditLog(
    action_type="UPDATE",
    table_name="alerts",
    record_id=alert.alert_id,
    description=(
        f"Alert review status changed to "
        f"{alert.review_status} for transaction "
        f"{alert.transaction_id}"
        )
    )

    db.session.add(audit_log)
    db.session.commit()

    return jsonify({
        "message": "Alert status updated successfully",
        "alert_id": alert.alert_id,
        "transaction_id": alert.transaction_id,
        "review_status": alert.review_status
    })

