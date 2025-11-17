# Summary

**Focus:** Web security threats and the SSL/TLS protocol suite.

**Web Security:** Web servers are easy to deploy but complex and vulnerable; may serve as entry points for attackers.

**OSI Context:**

- IPsec → Network layer security
- SSL/TLS → Transport/Application layer
- Kerberos → Application layer (over UDP)

**SSL/TLS Fundamentals:**

- Provide authentication, confidentiality, and integrity (e.g., HTTPS).
- TLS evolved from SSL with stronger algorithms and better configurability.

**TLS Architecture:**

- Session: crypto parameters (master secret, cipher suite).
- Connection: specific encryption/MAC keys, IVs, sequence numbers.

**TLS Protocols:**

- Record Protocol – encryption, compression, MAC.
- Handshake – negotiates keys, ciphers, authentication (4 stages).
- Change Cipher Spec – activates new crypto state.
- Alert – handles warnings and fatal errors.
- Heartbeat – maintains idle sessions.

**Vulnerability:** Heartbleed bug in OpenSSL’s Heartbeat allowed leakage of memory contents (keys, credentials) from $\approx \frac{2}{3}$ of web servers.
