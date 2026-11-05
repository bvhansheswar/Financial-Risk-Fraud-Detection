USE financial_risk_db;

-- ============================================
-- CUSTOMERS
-- ============================================

INSERT INTO customers (customer_id, customer_code) VALUES
(1, 'CUST001'),
(2, 'CUST002'),
(3, 'CUST003'),
(4, 'CUST004'),
(5, 'CUST005'),
(6, 'CUST006'),
(7, 'CUST007'),
(8, 'CUST008'),
(9, 'CUST009'),
(10, 'CUST010');


-- ============================================
-- ACCOUNTS
-- ============================================

INSERT INTO accounts (account_id, customer_id) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);


-- ============================================
-- TRANSACTIONS
-- ============================================

INSERT INTO transactions
(transaction_id, account_id, transaction_datetime, amount,
 transaction_type, channel, region)
VALUES

(1, 1, '2026-10-01 09:15:00', 2500.00,
 'Debit', 'ATM', 'Hyderabad'),

(2, 1, '2026-10-01 10:20:00', 1800.00,
 'Debit', 'POS', 'Hyderabad'),

(3, 1, '2026-10-01 11:05:00', 2200.00,
 'Debit', 'Online', 'Hyderabad'),

(4, 2, '2026-10-02 09:30:00', 4500.00,
 'Credit', 'Bank Transfer', 'Bengaluru'),

(5, 2, '2026-10-02 13:10:00', 3200.00,
 'Debit', 'POS', 'Bengaluru'),

(6, 3, '2026-10-03 10:00:00', 7500.00,
 'Debit', 'Online', 'Chennai'),

(7, 3, '2026-10-03 10:15:00', 8200.00,
 'Debit', 'Online', 'Chennai'),

(8, 3, '2026-10-03 10:30:00', 9100.00,
 'Debit', 'Online', 'Chennai'),

(9, 4, '2026-10-04 12:45:00', 15000.00,
 'Debit', 'Online', 'Mumbai'),

(10, 4, '2026-10-04 14:20:00', 1200.00,
 'Debit', 'POS', 'Mumbai'),

(11, 5, '2026-10-05 08:30:00', 2700.00,
 'Credit', 'Bank Transfer', 'Delhi'),

(12, 5, '2026-10-05 17:40:00', 3100.00,
 'Debit', 'ATM', 'Delhi'),

(13, 6, '2026-10-06 16:20:00', 25000.00,
 'Debit', 'Online', 'Hyderabad'),

(14, 7, '2026-10-07 11:15:00', 18500.00,
 'Debit', 'Online', 'Pune'),

(15, 7, '2026-10-07 11:20:00', 19500.00,
 'Debit', 'Online', 'Pune'),

(16, 8, '2026-10-08 09:45:00', 900.00,
 'Debit', 'POS', 'Hyderabad'),

(17, 8, '2026-10-08 09:50:00', 950.00,
 'Debit', 'POS', 'Hyderabad'),

(18, 8, '2026-10-08 09:55:00', 1100.00,
 'Debit', 'POS', 'Hyderabad'),

(19, 9, '2026-10-09 15:30:00', 3000.00,
 'Credit', 'Bank Transfer', 'Kolkata'),

(20, 10, '2026-10-10 18:00:00', 45000.00,
 'Debit', 'Online', 'Delhi');


-- ============================================
-- ALERTS
-- ============================================

INSERT INTO alerts
(alert_id, transaction_id, rule_name, risk_score, review_status, reason)
VALUES

(1, 6, 'High Frequency', 30.00,
 'Pending', 'Multiple transactions detected within a short time period.'),

(2, 7, 'High Frequency', 30.00,
 'Pending', 'Multiple transactions detected within a short time period.'),

(3, 8, 'High Frequency', 30.00,
 'Pending', 'Multiple transactions detected within a short time period.'),

(4, 9, 'Unusual Amount', 40.00,
 'Pending', 'Transaction amount exceeds the configured amount threshold.'),

(5, 13, 'Unusual Amount', 40.00,
 'Pending', 'Transaction amount exceeds the configured amount threshold.'),

(6, 14, 'Unusual Amount', 40.00,
 'Pending', 'Transaction amount exceeds the configured amount threshold.'),

(7, 15, 'High Frequency', 30.00,
 'Pending', 'Multiple transactions detected within a short time period.'),

(8, 20, 'Unusual Amount', 40.00,
 'Pending', 'Transaction amount exceeds the configured amount threshold.');


-- ============================================
-- AUDIT LOGS
-- ============================================

INSERT INTO audit_logs
(action_type, table_name, record_id, description)
VALUES

('INSERT', 'customers', 1, 'Customer CUST001 created'),
('INSERT', 'customers', 2, 'Customer CUST002 created'),
('INSERT', 'customers', 3, 'Customer CUST003 created'),
('INSERT', 'customers', 4, 'Customer CUST004 created'),
('INSERT', 'accounts', 1, 'Account 1 created for customer 1'),
('INSERT', 'accounts', 2, 'Account 2 created for customer 2'),
('INSERT', 'transactions', 1, 'Transaction 1 recorded'),
('INSERT', 'transactions', 6, 'High-frequency transaction recorded'),
('INSERT', 'transactions', 9, 'High-value transaction recorded'),
('INSERT', 'transactions', 13, 'High-value transaction recorded'),
('ALERT', 'alerts', 1, 'High-frequency alert generated'),
('ALERT', 'alerts', 4, 'Unusual amount alert generated'),
('ALERT', 'alerts', 5, 'Unusual amount alert generated'),
('ALERT', 'alerts', 8, 'Unusual amount alert generated');


-- ============================================
-- VERIFY DATA
-- ============================================

SELECT * FROM customers;

SELECT * FROM accounts;

SELECT * FROM transactions;

SELECT * FROM alerts;

SELECT * FROM audit_logs;