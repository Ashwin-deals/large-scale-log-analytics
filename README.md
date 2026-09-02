# Large-Scale Log Analytics for Cloud Security

## Overview
This project focuses on building an evolutionary real-time log analytics system for detecting anomalies in cloud environments using streaming technologies and machine learning.

## Objective
To design a SIEM-inspired system capable of:
- Real-time log ingestion
- Behavioral anomaly detection
- Evolutionary optimization using Genetic Algorithms
- Security alert generation

## Proposed Architecture
Application → Streaming Engine → Feature Processing → ML Model → Alert System

## Technologies
- Python
- Django
- Apache Kafka / Apache Flink
- Pandas
- Scikit-learn
- PyGAD (Genetic Algorithm)
- PostgreSQL
- Docker
- Chart.js

## Project Status
Phase 1: Architecture Design & Tool Selection

## Auth API (login/register)
A minimal Flask + MongoDB service backs the frontend login page.

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # set MONGO_URI / JWT_SECRET as needed
python app.py           # runs on http://localhost:5000
```

Requires a running MongoDB instance (local or Atlas) reachable at `MONGO_URI`. Passwords are hashed with bcrypt before storage — plaintext passwords are never persisted.

Endpoints:
- `POST /api/auth/register` — `{ email, password, name }`
- `POST /api/auth/login` — `{ email, password }`
- `GET /api/health`

## Team Members
Akilan J [CB.SC.U4CSE23002]
Ashwin V [CB.SC.U4CSE23009]
E Raksha Raj [CB.SC.U4CSE23021]
Mithresh M [CB.SC.U4CSE23039]
