# Summary

## Kerberos

- **Goal:** Efficient authentication using only symmetric cryptography with the help of a Trusted Third Party (KDC).
- **Motivation:**
    - Public-key systems are slow.
    - Symmetric systems need $N^2$  keys.
    - Kerberos uses only  N keys — one per user with the KDC.
- **Core Mechanism:**
    - KDC shares a secret key with each user.
    - Users obtain a Ticket-Granting Ticket (TGT) on login.
    - TGT used to request service tickets for specific resources.
- **Security:**
    Uses session keys and timestamps for confidentiality and replay protection.
    KDC is the single point of trust — must remain secure.
- **Advantages:**
    - No PKI needed.
    - Stateless and scalable.
    - Transparent authentication for users.
