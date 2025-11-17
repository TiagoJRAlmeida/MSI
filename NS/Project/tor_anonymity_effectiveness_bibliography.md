# 🧠 State of the Art on Tor: Assessing Anonymity Effectiveness

## 🎯 Project Context
This bibliography and reading plan support a report analyzing **how effective Tor is at providing anonymity**.  
It emphasizes Tor’s design, anonymity mechanisms, attack vectors, empirical evaluations, and modern improvements.

---

## 🧱 1. Foundational Context – How Tor Works

| Purpose | Paper | Citation |
|----------|--------|-----------|
| Explain the onion routing concept | *Hiding Routing Information* | Goldschlag, D. M., Reed, M. G., & Syverson, P. F. (1996). Communications of the ACM, 42(2), 39–41. |
| Early anonymous connection model | *Anonymous Connections and Onion Routing* | Reed, M. G., Syverson, P. F., & Goldschlag, D. M. (1998). IEEE JSAC, 16(4), 482–494. |
| Core Tor architecture | *Tor: The Second-Generation Onion Router* | Dingledine, R., Mathewson, N., & Syverson, P. (2004). USENIX Security Symposium. |
| Hidden services overview | *Locating Hidden Servers* | Øverlier, L., & Syverson, P. (2006). IEEE Symposium on Security and Privacy. |

---

## 🕵️‍♂️ 2. Core to Assessing Effectiveness – Attacks & Defenses

| Focus | Paper | Citation |
|--------|--------|-----------|
| Traffic analysis attacks | *Low-Cost Traffic Analysis of Tor* | Murdoch, S. J., & Danezis, G. (2005). IEEE Symposium on Security and Privacy. |
| Routing and resource attacks | *Low-Resource Routing Attacks Against Tor* | Bauer, K., McCoy, D., Grunwald, D., Kohno, T., & Sicker, D. (2007). ACM WPES. |
| End-to-end correlation | *Users Get Routed: Traffic Correlation on Tor* | Johnson, A., Wacek, C., Jansen, R., Sherr, M., & Syverson, P. (2013). ACM CCS. |
| Entry guard defense | *Guard Sets for Tor Entry Guards* | Jansen, R., Johnson, A., & Syverson, P. (2014). ACM CCS. |
| Real-world measurement | *Measuring the Privacy and Performance of Onion Services in the Wild* | Jansen, R., et al. (2023). USENIX Security Symposium. |

---

## ⚙️ 3. Supplementary for Evaluation & Practical Work

| Purpose | Paper | Citation |
|----------|--------|-----------|
| Tor simulation | *Shadow: Running Tor in a Box* | Jansen, R., Hopper, N., & Dingledine, R. (2013). USENIX Security Symposium. |
| Understanding metrics | *Tor Metrics Portal* | Tor Project Metrics Team. (2022). [https://metrics.torproject.org](https://metrics.torproject.org) |
| Performance vs anonymity | *Performance Analysis of Tor with Modern Internet Conditions* | Fischer, R., & Wacek, C. (2020). Computers & Security, 92. |
| Broader survey | *Survey on Tor Network: Architecture, Attacks, and Research Opportunities* | Ren, Y., & Wu, L. (2019). IEEE Communications Surveys & Tutorials. |

---

## 📚 4. Optional Contextual Papers

| Focus | Paper | Citation |
|--------|--------|-----------|
| Anonymity systems survey | *On the Anonymity of Anonymity Systems* | Edman, M., & Yener, B. (2009). ACM Transactions on Information and System Security. |
| Future directions | *The Future of Anonymous Communication Networks* | Das, A., et al. (2024). Journal of Cybersecurity. |
| Social implications | *Do You See Me Now? Website Treatment of Tor Users* | Matic, S., et al. (2018). Privacy Enhancing Technologies Symposium (PETS). |

---

## 🧩 6. Suggested Report Structure

1. **Introduction** – Motivation and problem statement.  
2. **Background** – Onion routing and early Tor development.  
3. **Mechanisms for anonymity** – Path selection, encryption layers, entry guards.  
4. **Threats & attacks** – Known anonymity-breaking techniques.  
5. **Effectiveness assessment** – What studies show about Tor’s real-world anonymity.  
6. **Discussion & Future Work** – How anonymity can be improved further.  
7. **Conclusion** – Balanced evaluation of Tor’s effectiveness.

---