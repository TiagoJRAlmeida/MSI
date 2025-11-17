# Summary

## Secure Shell (SSH)

- Secure protocol for remote command-line access.
- Replaces insecure tools like Telnet, rlogin, and rsh.
- Composed of three layered protocols:
    - **Transport Layer Protocol:** provides server authentication, confidentiality, and integrity.
    - **User Authentication Protocol:** authenticates the user via public key, password, or host-based methods.
    - **Connection Protocol:** multiplexes the encrypted tunnel into multiple logical channels (e.g., terminal session, X11, TCP forwarding).
- Supports **SSH tunneling (port forwarding)** to secure arbitrary TCP connections.

 
## IPSec (Internet Protocol Security)

- Operates at the **network layer**, transparent to applications.
- Provides **authentication, confidentiality, and key management**.
- Used in **VPNs**, secure remote access, and inter-network communication.
- Two main protocol components:
    - **AH (Authentication Header)**: provides integrity only.
    - **ESP (Encapsulating Security Payload)**: provides both confidentiality and integrity.
- Two modes of operation:
    - **Transport Mode:** protects only the IP payload.
    - **Tunnel Mode:** encapsulates the entire IP packet.
- Relies on the **IKE (Internet Key Exchange)** protocol for negotiation:
    - **Phase 1:** establishes an IKE Security Association (SA).
    - **Phase 2:** establishes the IPSec SA with session keys.
- Security associations are managed using **SAD** and **SPD**.
- Complex to configure; not always firewall-friendly.
