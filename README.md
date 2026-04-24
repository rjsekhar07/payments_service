# Payment Reconciliation Service

## 🚀 Live Demo

**Base URL:** https://payments-service-9o9x.onrender.com
**Swagger Docs:** https://payments-service-9o9x.onrender.com/docs

---

## 📌 Overview

This project implements an **event-driven payment reconciliation system** using FastAPI and MySQL.

It ingests payment events, maintains transaction states, and provides reconciliation insights such as summaries and discrepancy detection.

---

## 🏗️ Architecture

```text
Client (Postman / Script)
        ↓
FastAPI Backend (Render)
        ↓
SQLAlchemy ORM
        ↓
MySQL Database (Railway)
```

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **Database:** MySQL (Railway)
* **ORM:** SQLAlchemy
* **Deployment:** Render
* **Data Loader:** Python (`load_data.py`)

---

## 📡 API Endpoints

### 🔹 Events

* `POST /events` → Ingest event
* `GET /events/{event_id}` → Fetch event by ID

---

### 🔹 Transactions

* `GET /transactions` → Fetch transactions with:

  * filtering (merchant_id, status)
  * date range (created_at)
  * pagination (skip, limit)
  * sorting

* `GET /transactions/{txn_id}` → Fetch transaction by ID

---

### 🔹 Reconciliation

* `GET /reconciliation/summary` → Aggregated counts

* `GET /reconciliation/discrepancies` → Detect inconsistencies

  ✅ Supports optional filter:

```text
type = processed_not_settled | failed_but_settled | conflicting_transactions
```

---

## 🧪 Example Request

### POST /events

```json
{
  "event_id": "evt_12345",
  "transaction_id": "txn_123",
  "merchant_id": "m_001",
  "amount": 100,
  "currency": "INR",
  "event_type": "payment_processed",
  "timestamp": "2026-04-02T02:34:10.184474+00:00"
}
```

---

## 🔁 Idempotency

* Duplicate events (same `event_id`) are ignored
* Ensures consistent transaction state
* Implemented via application-level checks

---

## 📊 SQL Design

* Filtering, sorting, and pagination handled in SQL
* Aggregations done using SQL (`GROUP BY`)

### Indexing (considered)

Indexes were considered on:

```text
event_id
transaction_id
merchant_id
created_at
```

---

## 📥 Data Loading

Simulate ingestion:

```bash
python load_data.py
```

* Processes 10,000+ events
* Demonstrates idempotency and system stability

---

## 🛠️ Local Setup

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

### 4. Set DB URL

```bash
export DATABASE_URL="your_mysql_connection_string"
```

### 5. Run server

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Testing

* Swagger UI (`/docs`)
* Postman collection included
* Tested with large dataset (10k+ events)

---

## 📬 Postman Collection

A Postman collection is provided to test all APIs easily.

### 📦 Files Included

* `postman_collection.json`
* `postman_environment.json`

### ⚙️ Setup Instructions

1. Open Postman
2. Import both files:

   * Collection file
   * Environment file
3. Select the environment from the top-right dropdown
4. Ensure `base_url` is set correctly:

```text
https://payments-service-9o9x.onrender.com
```

### ▶️ Usage

* Use the predefined requests to test all APIs
* Query parameters are pre-configured for filtering
* Duplicate event request included to demonstrate idempotency

### 🧪 Covered APIs

* Event ingestion (`POST /events`)
* Duplicate handling
* Transaction queries (with filters & pagination)
* Reconciliation summary
* Discrepancy detection (with optional type filter)

---

## ⚖️ Assumptions

* Each event has a unique `event_id`
* Transaction state derived from events
* Data consistency prioritized over real-time streaming

---

## 🔄 Tradeoffs

* Used synchronous FastAPI for simplicity
* No batch ingestion (kept design simple)
* Application-level idempotency instead of DB constraints
* Used Railway free tier for quick setup

---

## 🚀 Future Improvements

* Add DB-level unique constraints
* Async processing / queue system
* Batch ingestion endpoint
* Authentication & rate limiting

---

## 🤖 AI Usage Disclosure

AI tools were used for:

* debugging deployment issues
* improving API structure
* refining documentation

All implementation decisions were validated and executed independently.

---

## ✅ Summary

* Processed **10,000+ events**
* Implemented **idempotent event handling**
* Built **scalable SQL-based APIs**
* Deployed a **fully working public service**

---

## 🎥 Demo Video

A walkthrough of the system is available here:

👉 loom link: https://www.loom.com/share/a560e0dca0f0474ca18f9cda78c6bc48
👉 Google drive link: https://drive.google.com/file/d/1LmJ-ELpqV5VGsERhPpASKjUd-zbc58ow/view?usp=sharing

The demo covers:

* Event ingestion
* Duplicate handling (idempotency)
* Transactions API with filters
* Reconciliation summary
* Discrepancy detection with optional filtering

---


## 📎 Submission Includes

* GitHub Repository
* Postman Collection
* Demo Video
* Live Deployment

---

**Author:** Sekhar
