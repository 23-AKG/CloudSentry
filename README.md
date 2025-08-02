# **CloudSentry – Real-Time Security Event Detection**

CloudSentry is a lightweight real-time security event detection system built using Python microservices and Apache Kafka.
It ingests events, applies detection rules (like brute-force login detection), and raises alerts automatically.

---

## **📌 Badges**

![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)
![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Kafka](https://img.shields.io/badge/Kafka-3.5-black?logo=apachekafka)
![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)


---

## **📌 Architecture**

![Architecture Diagram](A_flowchart_diagram_in_the_image_titled_"CloudSent.png")

---

## **📂 Project Structure**

```
cloudsentry/
│── docker-compose.yml          # Orchestration for all services + Kafka + Zookeeper
│── services/
│   ├── ingest_service/         # Reads sample events & publishes to Kafka
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── sample_events.json
│   │
│   ├── detect_service/         # Consumes events, applies detection logic
│   │   ├── app.py
│   │   ├── rules.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── alert_service/          # Consumes alerts & logs notifications
│   │   ├── app.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── common/                 # Shared utilities (logging, Kafka setup)
│       ├── __init__.py
│       └── utils.py
│
└── quick_test.py               # Optional script to test the pipeline
```

---

## **🚀 Getting Started**

### **1️⃣ Prerequisites**

* Docker & Docker Compose installed
* Python 3.11+ (only for running `quick_test.py` locally, optional)

---

### **2️⃣ Start the System**

```bash
docker-compose up --build
```

This will:

* Start **Zookeeper** and **Kafka**
* Build and run:

  * `ingest_service`
  * `detect_service`
  * `alert_service`

---

### **3️⃣ How It Works**

* **Ingest Service** reads `sample_events.json` and pushes events to Kafka topic `events`.
* **Detect Service** consumes from `events`, applies rules (e.g. brute force detection), and publishes alerts to `alerts`.
* **Alert Service** consumes from `alerts` and logs alerts.

---

### **4️⃣ Logs & Verification**

Check logs to verify the pipeline:

```bash
docker logs ingest_service -f
docker logs detect_service -f
docker logs alert_service -f
```

Expected output:

```
IngestService: ✅ Sent: { ... }
DetectService: 🚨 Alert Generated: { ... }
AlertService: 🚨 ALERT: { ... }
```

---

## **📊 Example Events (`sample_events.json`)**

```json
[
  {"timestamp": "2025-08-02T10:00:00", "ip": "192.168.0.10", "event": "failed_login"},
  {"timestamp": "2025-08-02T10:00:05", "ip": "192.168.0.10", "event": "failed_login"},
  {"timestamp": "2025-08-02T10:00:10", "ip": "192.168.0.10", "event": "failed_login"},
  {"timestamp": "2025-08-02T10:01:00", "ip": "10.0.0.5", "event": "login_success"},
  {"timestamp": "2025-08-02T10:02:00", "ip": "203.0.113.45", "event": "suspicious_activity"}
]
```

---

## **✅ Test the Pipeline (Optional)**

Run a quick test to publish and consume events without restarting services:

```bash
python quick_test.py
```

---

## **🛑 Stopping the System**

```bash
docker-compose down
```

---
