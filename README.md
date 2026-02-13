# Rate Limiting Service (FastAPI + Redis)

Production-style rate limiting service with **per-user** and **per-endpoint** enforcement, **4 algorithms**, **metrics**, and a small **web playground UI**.

**Live Demo:** https://rate-limiter-wpef.onrender.com/  


---

## What this project does

This service protects APIs from abuse (spamming, brute-force, traffic spikes) by limiting how many requests a user can make.

✅ Per-user enforcement via request header: `X-User-Id`  
✅ Different limits per endpoint (policy-based)  
✅ Algorithm chosen dynamically (strategy pattern)  
✅ Redis-backed state + **atomic** updates using Lua scripts  
✅ Metrics endpoint for observability  
✅ Deployed on Render (public demo link)

---

## Algorithms supported

- **Fixed Window** — counter resets every time window (simple + fast)
- **Sliding Window** — counts requests within the last N seconds (fairer)
- **Token Bucket** — refills tokens over time (allows bursts, controls average)
- **Leaky Bucket** — leaks at a constant rate (smooth traffic, prevents bursts)

---

## How it works (high-level)

Client (UI / Swagger / API call)
↓
FastAPI route
↓
Policy lookup (per endpoint)
↓
LimiterSelector chooses algorithm
↓
Redis (counters/state, atomic Lua scripts)
↓
Allow (200) or Block (429)
↓
Metrics updated


---

## Quick test (multi-user)

Use the UI at:

https://rate-limiter-wpef.onrender.com/

1. Set **User ID = alice**, click `/login` repeatedly → eventually gets **429**
2. Change **User ID = bob** → works again (separate counter)

---

## Endpoints

- `GET /` → Playground UI  
- `GET /docs` → Swagger UI  
- `GET /login`, `GET /data`, `GET /analyze` → demo endpoints with different policies  
- `GET /metrics` → allowed/blocked counters

---

## Run locally

### 1) Install dependencies
```bash
pip install -r requirements.txt
2) Start Redis
redis-server
Verify:

redis-cli ping
# PONG
3) Start FastAPI
uvicorn app.main:app --reload
Open:

http://127.0.0.1:8000/ (UI)

http://127.0.0.1:8000/docs (Swagger)

Tech stack
FastAPI, Uvicorn

Redis (state + metrics)

Redis Lua scripts (atomic algorithm operations)

Render (deployment)

Static HTML/JS (playground UI)

