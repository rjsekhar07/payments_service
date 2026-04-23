# 🚀 Payment Reconciliation System

## 🔹 Overview

This project is an event-driven payment processing and reconciliation system built using FastAPI and MySQL.

It simulates how modern payment gateways process events such as payment initiation, processing, failures, and settlements, while ensuring data integrity and reconciliation.

---

## 🔹 Key Features

* Event-driven architecture
* Idempotent event ingestion (duplicate-safe)
* Transaction state tracking
* Reconciliation and discrepancy detection
* RESTful APIs with filtering support
* Handles 10,000+ events efficiently

---

## 🔹 Architecture

```
Events (JSON / API)
        ↓
FastAPI (Routes)
        ↓
Service Layer (Business Logic)
        ↓
MySQL Database
        ↓
Reconciliation APIs
```

---

## 🔹 Database Design

### Tables

### 1. events

* Stores all incoming events (source of truth)
* Ensures idempotency using unique `event_id`

### 2. transactions

* Maintains current transaction state
* Updated based on latest event

### 3. merchants

* Stores merchant details

---

## 🔹 Idempotency

Idempotency is implemented using:

* Unique constraint on `event_id`
* Pre-insert check to avoid duplicate processing

If the same event is received again:

```json
{
  "status": "duplicate"
}
```

---

## 🔹 APIs

### 1. Ingest Event

```
POST /events
```

### 2. Get Transactions

```
GET /transactions
```

Supports filters:

* merchant_id
* status
* pagination (skip, limit)

---

### 3. Get Transaction Details

```
GET /transactions/{transaction_id}
```

---

### 4. Reconciliation Summary

```
GET /reconciliation/summary
```

Returns count of transactions grouped by merchant and status.

---

### 5. Reconciliation Discrepancies

```
GET /reconciliation/discrepancies
```



---

## 🔹 Discrepancy Cases Covered

* Processed but not settled
* Failed but settled
* Conflicting state transitions (advanced case)

---

## 🔹 Local Setup

### 1. Clone repo

```bash
git clone https://github.com/rjsekhar07/payments_service.git
cd payments_service
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variable

```bash
export DATABASE_URL="mysql+pymysql://user:password@localhost/payments_db"
```

### 5. Run server

```bash
uvicorn app.main:app --reload
```

### 6. Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 🔹 Load Sample Data

```bash
python load_data.py
```

System successfully processed **10,000+ events with idempotent handling and zero failures**.

---

## 🔹 Deployment

* Backend hosted on Render
* Database hosted on Railway

Public URL:

```
<your-deployed-url>
```

---

## 🔹 Assumptions

* Latest event determines transaction state
* Event ordering handled using priority logic
* Duplicate events are ignored safely

---

## 🔹 Tradeoffs

* Some reconciliation logic implemented in Python for clarity (can be optimized using SQL)
* No asynchronous processing (kept simple for scope)

---

## 🔹 Future Improvements

* Kafka-based event streaming
* Redis caching
* Bulk ingestion endpoint
* Advanced state machine validation

---

## 🔹 AI Usage Disclosure

ChatGPT was used for:

* Debugging issues
* Designing architecture
* Improving code structure
* Writing documentation

---

## 🔹 Author

Sekhar Pidugu
