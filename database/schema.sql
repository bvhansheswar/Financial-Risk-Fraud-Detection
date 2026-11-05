CREATE DATABASE IF NOT EXISTS financial_risk_db;

USE financial_risk_db;


CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_code VARCHAR(20) NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS accounts (
    account_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);


CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INT PRIMARY KEY AUTO_INCREMENT,
    account_id INT NOT NULL,
    transaction_datetime DATETIME NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    channel VARCHAR(30) NOT NULL,
    region VARCHAR(100),
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);



CREATE TABLE IF NOT EXISTS alerts (
    alert_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    rule_name VARCHAR(100) NOT NULL,
    risk_score DECIMAL(5,2) NOT NULL,
    review_status VARCHAR(30) NOT NULL DEFAULT 'Pending',
    reason VARCHAR(255),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
);


CREATE TABLE IF NOT EXISTS audit_logs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    action_type VARCHAR(50) NOT NULL,
    table_name VARCHAR(50) NOT NULL,
    record_id INT,
    action_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS alerts (
    alert_id INT PRIMARY KEY AUTO_INCREMENT,
    transaction_id INT NOT NULL,
    rule_name VARCHAR(100) NOT NULL,
    risk_score FLOAT NOT NULL,
    reason VARCHAR(255) NOT NULL,
    review_status VARCHAR(30) NOT NULL DEFAULT 'Pending',

    FOREIGN KEY (transaction_id)
        REFERENCES transactions(transaction_id)
);

SHOW TABLES;