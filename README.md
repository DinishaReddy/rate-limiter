📦 Rate Limiting Service (FastAPI + Redis + Multiple Algorithms)

A production-style rate limiting service built with FastAPI, Redis, and multiple rate limiting algorithms.
The system enforces per-user, per-endpoint limits, supports dynamic algorithm selection, exposes real-time metrics, and includes an interactive frontend playground.

🚀 Live Demo

Frontend Playground: https://your-app.onrender.com/

Swagger Docs: https://your-app.onrender.com/docs

(Replace your-app with your actual Render service name.)

🧠 Problem Statement

APIs must protect themselves from abuse such as:

Brute-force login attempts

Traffic spikes

Automated scraping

Denial-of-service patterns

This project implements a flexible and production-ready rate limiting system that:

Controls request frequency

Applies different rules per endpoint

Enforces limits per user

Ensures atomic updates under concurrency

Provides observability via metrics

🏗 Architecture
Client (Browser / API / UI)
        ↓
FastAPI Server
        ↓
Limiter Selector (Strategy Pattern)
        ↓
Rate Limiting Algorithm
        ↓
Redis (State + Atomic Lua Scripts)
        ↓
Decision (Allow / 429)
        ↓
Metrics Recorded

✨ Features

✅ Per-user enforcement (X-User-Id)

✅ Per-endpoint rate limit policies

✅ Multiple rate limiting algorithms:

Fixed Window

Sliding Window

Token Bucket

Leaky Bucket

✅ Redis-backed storage

✅ Atomic operations using Redis Lua scripts

✅ Metrics endpoint (/metrics)

✅ Interactive frontend playground (/)

✅ Swagger documentation (/docs)

✅ Deployed publicly on Render

⚙️ Rate Limiting Algorithms
1️⃣ Fixed Window

Counts requests in fixed time buckets. Simple and efficient, but can allow boundary spikes.

2️⃣ Sliding Window

Tracks requests within the last N seconds. More accurate and fair; implemented with Redis sorted sets.

3️⃣ Token Bucket

Tokens refill over time. Allows short bursts while controlling average request rate.

4️⃣ Leaky Bucket

Processes requests at a steady rate. Smooths traffic and prevents bursts.

📜 Endpoint Policies

Each endpoint defines:

max_requests

window_seconds

algorithm

Example policy mapping in code:

"/login":   5 requests / 60s (sliding_window)
"/data":    60 requests / 60s (token_bucket)
"/analyze": 10 requests / 60s (leaky_bucket)


Policies are configuration only — the selector picks the algorithm at runtime.

📊 Metrics

The service tracks:

Total allowed requests

Total blocked requests

Per-endpoint activity

Metrics are stored in Redis and exposed at:

GET /metrics


Example response:

{
  "allowed_requests": 23,
  "blocked_requests": 22
}

🖥 Frontend Playground

A built-in UI at / that lets you:

Enter a User ID

Call /login, /data, /analyze via buttons

See response status and JSON output

View metrics live

This demo page is for easy manual testing (no Postman needed).

🧰 Tech Stack

Backend: FastAPI

Storage: Redis (Key-Value)

Concurrency Safety: Redis Lua scripts

Deployment: Render

Frontend: Static HTML + JavaScript

🏃‍♂️ Run Locally
1. Install dependencies
pip install -r requirements.txt

2. Start Redis
redis-server


Verify:

redis-cli ping
# PONG

3. Start FastAPI
uvicorn app.main:app --reload


Open:

http://127.0.0.1:8000/
 → Playground UI

http://127.0.0.1:8000/docs
 → Swagger

🌍 Deployment (Render)

Key points for Render deployment:

Use Render Key-Value (managed Redis) and copy the provided URL into the web service REDIS_URL environment variable.

Start command for the Web Service:

uvicorn app.main:app --host 0.0.0.0 --port $PORT


Render will pull from GitHub, build dependencies from requirements.txt, and run the service.

🧩 Design Patterns & Principles

Strategy Pattern — dynamic algorithm selection per policy

Separation of Concerns — policies, algorithms, Redis client, and routes are modular

Configuration-driven — policies live in a single place for easy changes

Atomic Redis scripting — ensures correctness under concurrency

🎯 Why This Project Matters

This project demonstrates:

Practical backend system design for API protection

Distributed state management with Redis

Concurrency-safe algorithms using Redis Lua scripts

Deployment and observability best practices
