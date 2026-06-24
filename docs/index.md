---
title: CipherToken - High-performance JWT and Cryptography Library
description: Fast Python JWT library built with Rust. Secure token generation, validation, and key management for authentication systems.
keywords: jwt, python, rust, cryptography, authentication, token, security, hmac, rsa
image: https://cipherunits.github.io/CipherToken/logo.png
---

# CipherToken

**CipherToken** is a next-generation token engine for developers who demand speed, security, and reliability. Unlike conventional JWT libraries, CipherToken delivers a complete token lifecycle — from creation and decoding to rotation and expiry tracking — all backed by the raw performance of **Rust**.

---

# CipherToken Benchmark

## Fast Python JWT Library Benchmark

CipherToken is a high-performance Python token library designed for applications that require fast token creation and verification with minimal overhead.

This benchmark compares CipherToken against popular Python JWT libraries using the HS256 algorithm.

## Benchmark Summary

🏆 **CipherToken achieved the highest performance in every benchmark category tested.**

| Library | Token Creation (ops/sec) | Token Verification (ops/sec) |
|----------|----------:|----------:|
| **CipherToken** | **587,156** | **244,500** |
| PyJWT | 101,591 | 35,928 |
| python-jose | 103,861 | 27,638 |

## Performance Advantage

### Token Creation

- CipherToken is **5.78x faster** than PyJWT.
- CipherToken is **5.65x faster** than python-jose.

### Token Verification

- CipherToken is **6.80x faster** than PyJWT.
- CipherToken is **8.85x faster** than python-jose.

## Benchmark Environment

- Python 3.14
- HS256 algorithm
- 100,000 iterations per benchmark
- Average of 5 runs
- Identical payload for all libraries

### Payload

```python
{
    "user_id": 123,
    "username": "ehsan",
    "role": "admin"
}
```

## Why CipherToken Is Faster

CipherToken is designed with performance as a primary goal.

Key optimizations include:

- Minimal runtime overhead
- Efficient token generation
- Optimized token verification
- Modern implementation focused on high throughput
- Suitable for APIs, authentication services, and microservices

## Real-World Benefits

Higher throughput means:

- Faster API responses
- Lower CPU usage
- Better scalability
- More requests handled per server
- Reduced infrastructure costs

## Benchmark Notes

The benchmark was executed on the same machine under identical conditions.

Results may vary depending on:

- Hardware
- Python version
- Payload size
- Selected algorithm
- Application workload

However, the benchmark consistently showed CipherToken outperforming the compared libraries in both token creation and verification workloads.

## Conclusion

For applications requiring fast token operations, CipherToken demonstrated the strongest performance in this benchmark, achieving significantly higher throughput than PyJWT and python-jose while maintaining a simple developer experience.


## Why CipherToken?

| | Conventional JWT Libraries | CipherToken |
|---|---|---|
| **Language** | Pure Python | Rust + PyO3 |
| **Performance** | Interpreted overhead | Near-native speed |
| **Async** | Often limited or absent | Fully async (Tokio) |
| **Token lifecycle** | Generate / verify | Create · Decode · Verify · Rotate · Inspect |
| **Key management** | Manual | Built-in HMAC + RSA key generation |
| **Expiry tracking** | Manual | Built-in (`remaining_time`) |

---

## Quick Install

```bash
pip install ciphertoken
```

---

## Quick Example

```python
from ciphertoken import CipherToken
from ciphertoken.algorithms import HS256
from ciphertoken.time import minutes, days
from ciphertoken.jwt import access, refresh, rotation

token = CipherToken(
    secret="your-strong-secret-key",
    algorithm=HS256,
    access_ttl=minutes(10),
    refresh_ttl=days(7),
)

access_token = access(token, payload={"user_id": 42})
refresh_token = refresh(token, payload={"user_id": 42})
new_access, new_refresh = rotation(token, refresh_token)

print(token.verify(access_token))  # True
```

---

## Get Started

<div class="grid cards" markdown>

-   :fontawesome-solid-download: [Installation](getting-started/installation.md) — pip, poetry, pdm, and more

-   :fontawesome-solid-bolt: [Quick Start](getting-started/quick-start.md) — Your first tokens in under 2 minutes

-   :fontawesome-solid-book: [API Reference](reference/index.md) — Complete module documentation

-   :fontawesome-solid-gear: [Advanced Guide](advanced/index.md) — Production best practices

</div>