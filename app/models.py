from app import db


class Customer(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    customer_code = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )


class Account(db.Model):
    __tablename__ = "accounts"

    account_id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.customer_id"),
        nullable=False
    )


class Transaction(db.Model):
    __tablename__ = "transactions"

    transaction_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    account_id = db.Column(
        db.Integer,
        db.ForeignKey("accounts.account_id"),
        nullable=False
    )

    transaction_datetime = db.Column(
        db.DateTime,
        nullable=False
    )

    amount = db.Column(
        db.Numeric(12, 2),
        nullable=False
    )

    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )

    channel = db.Column(
        db.String(30),
        nullable=False
    )

    region = db.Column(
        db.String(50),
        nullable=True
    )

class Alert(db.Model):
    __tablename__ = "alerts"

    alert_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    transaction_id = db.Column(
        db.Integer,
        db.ForeignKey("transactions.transaction_id"),
        nullable=False
    )

    rule_name = db.Column(db.String(100), nullable=False)

    risk_score = db.Column(db.Float, nullable=False)

    reason = db.Column(db.String(255), nullable=False)

    review_status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    log_id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    action_type = db.Column(
        db.String(50),
        nullable=False
    )

    table_name = db.Column(
        db.String(50),
        nullable=False
    )

    record_id = db.Column(
        db.Integer,
        nullable=True
    )

    action_datetime = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp()
    )

    description = db.Column(
        db.String(255),
        nullable=True
    )

    