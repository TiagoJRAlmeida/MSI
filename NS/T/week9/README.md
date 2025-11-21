# Week 9: Firewalls and Intrusion Detection Systems

This class focuses on two core components of network defence: **firewalls** and
**intrusion detection systems (IDS)**, including practical tools and attacker models.

# Firewalls

- **Firewall location and DMZ (Demilitarized Zone)**: positioning servers that require both internal and external access.
- **Defence in depth**: layering packet filters, application proxies, and bastion hosts to slow intrusions and support detection.
- **Firewall types**:
  - **Bastion hosts**: hardened network strongpoints with minimal services.
  - **Host-based firewalls**: rule-based protection on servers.
  - **Personal firewalls**: simple, local defences against unauthorised access.
- **Tools**:
  - **Firewalk**: a reconnaissance tool for detecting firewall rules via TTL manipulation.
  - **IPTables (Linux)**: managing access control rules using tables, chains, and targets (DROP, ACCEPT, REJECT, etc.).

# Intrusion Detection Systems (IDS)

- **Why IDS?**: Intrusions are still possible even with prevention. IDS detects suspicious or ongoing attacks.
- **Intruder types**:
  - **Cybercriminals** (financially motivated)
  - **State-sponsored APTs**
  - **Hacktivists**
  - **Recreational hackers**
  - **Insiders** (difficult to detect, motivated by revenge, profit, or ideology).
- **Detection strategies**:
  - Signature-based
  - Anomaly-based (e.g. statistical or ML-based detection)
