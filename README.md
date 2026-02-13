🚦 Rate Limiting Service

Production-style rate limiting system built with FastAPI, Redis, and multiple rate limiting algorithms.

🔗 Live Demo: https://rate-limiter-wpef.onrender.com/

📘 Swagger Docs: https://rate-limiter-wpef.onrender.com/docs

📊 Metrics: https://rate-limiter-wpef.onrender.com/metrics

📌 Overview

This project protects APIs from abuse such as:

Brute-force login attempts

Traffic spikes

Automated scraping

Request flooding

It enforces per-user and per-endpoint limits using configurable policies and multiple rate limiting strategies.

✨ Features

Per-user enforcement (X-User-Id header)

Configurable per-endpoint policies

Multiple rate limiting algorithms:

Fixed Window

Sliding Window

Token Bucket

Leaky Bucket

Redis-backed state management

Atomic operations using Redis Lua scripts

Metrics endpoint

Interactive frontend playground

Deployed publicly on Render

🧠 How It Works

Client (Browser / UI / Swagger)
↓
FastAPI Endpoint
↓
Policy Lookup (per endpoint)
↓
LimiterSelector (Strategy Pattern)
↓
Chosen Rate Limiting Algorithm
↓
Redis (State + Atomic Lua Script)
↓
Allow (200) or Block (429)
↓
Metrics Updated

⚙️ Algorithms Supported
Fixed Window

Counter resets every time window.
Simple and fast.

Sliding Window

Counts requests within the last N seconds.
More accurate and fair.

Token Bucket

Refills tokens over time.
Allows bursts while controlling average rate.

Leaky Bucket

Processes requests at a constant rate.
Prevents burst traffic.

📜 Example Policy Configuration
/login   → 5 requests / 60s  (sliding_window)
/data    → 60 requests / 60s (token_bucket)
/analyze → 10 requests / 60s (leaky_bucket)


Policies define:

Maximum requests

Time window

Algorithm to use

🖥 Playground UI

The root route / serves a frontend where you can:

Enter a custom User ID

Trigger endpoints

See response status

Watch metrics update live

📊 Metrics

The system tracks:

Total allowed requests

Total blocked requests

Example response:

{
  "allowed_requests": 23,
  "blocked_requests": 22
}

🧰 Tech Stack

FastAPI

Redis

Redis Lua Scripts

Uvicorn

Render

Static HTML + JavaScript

🏃 Run Locally

Install dependencies:

pip install -r requirements.txt


Start Redis:

redis-server


Start FastAPI:

uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000/
http://127.0.0.1:8000/docs

🎯 Why This Project Matters

This project demonstrates:

Backend system design

Distributed rate limiting

Concurrency-safe architecture

Cloud deployment

Observability via metrics

Clean modular structure
