# Rate Limiting Service (FastAPI + Redis)

Production-style rate limiting service with **per-user** and **per-endpoint** enforcement, **4 algorithms**, **metrics**, and a small **web playground UI**.

**Live Demo:** https://rate-limiter-wpef.onrender.com/  
**Swagger Docs:** https://rate-limiter-wpef.onrender.com/docs  
**Metrics:** https://rate-limiter-wpef.onrender.com/metrics

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

