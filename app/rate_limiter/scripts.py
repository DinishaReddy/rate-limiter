# app/rate_limiter/scripts.py

# Sliding Window (sorted set of timestamps)
# KEYS[1] = zset key
# ARGV[1] = now_ms
# ARGV[2] = window_ms
# ARGV[3] = max_requests
# ARGV[4] = member_id (unique)
SLIDING_WINDOW_LUA = """
local key = KEYS[1]
local now_ms = tonumber(ARGV[1])
local window_ms = tonumber(ARGV[2])
local max_requests = tonumber(ARGV[3])
local member_id = ARGV[4]

local cutoff = now_ms - window_ms

redis.call('ZREMRANGEBYSCORE', key, 0, cutoff)
local count = redis.call('ZCARD', key)

if count >= max_requests then
  redis.call('PEXPIRE', key, window_ms)
  return {0, count}
end

redis.call('ZADD', key, now_ms, member_id)
redis.call('PEXPIRE', key, window_ms)
return {1, count + 1}
"""

# Token Bucket
# KEYS[1] = token bucket key (hash)
# ARGV[1] = now_ms
# ARGV[2] = capacity
# ARGV[3] = refill_rate_per_ms  (tokens added per millisecond)
TOKEN_BUCKET_LUA = """
local key = KEYS[1]
local now_ms = tonumber(ARGV[1])
local capacity = tonumber(ARGV[2])
local refill_rate = tonumber(ARGV[3])

local tokens = redis.call('HGET', key, 'tokens')
local last_ms = redis.call('HGET', key, 'last_ms')

if tokens == false then
  tokens = capacity
else
  tokens = tonumber(tokens)
end

if last_ms == false then
  last_ms = now_ms
else
  last_ms = tonumber(last_ms)
end

local delta = now_ms - last_ms
if delta < 0 then delta = 0 end

local refill = delta * refill_rate
tokens = math.min(capacity, tokens + refill)

local allowed = 0
if tokens >= 1 then
  tokens = tokens - 1
  allowed = 1
end

redis.call('HSET', key, 'tokens', tokens)
redis.call('HSET', key, 'last_ms', now_ms)

return {allowed, tokens}
"""

# Leaky Bucket
# KEYS[1] = leaky bucket key (hash)
# ARGV[1] = now_ms
# ARGV[2] = capacity
# ARGV[3] = leak_rate_per_ms (leaks per millisecond)
LEAKY_BUCKET_LUA = """
local key = KEYS[1]
local now_ms = tonumber(ARGV[1])
local capacity = tonumber(ARGV[2])
local leak_rate = tonumber(ARGV[3])

local water = redis.call('HGET', key, 'water')
local last_ms = redis.call('HGET', key, 'last_ms')

if water == false then
  water = 0
else
  water = tonumber(water)
end

if last_ms == false then
  last_ms = now_ms
else
  last_ms = tonumber(last_ms)
end

local delta = now_ms - last_ms
if delta < 0 then delta = 0 end

local leaked = delta * leak_rate
water = math.max(0, water - leaked)

local allowed = 0
if water + 1 <= capacity then
  water = water + 1
  allowed = 1
end

redis.call('HSET', key, 'water', water)
redis.call('HSET', key, 'last_ms', now_ms)

return {allowed, water}
"""
