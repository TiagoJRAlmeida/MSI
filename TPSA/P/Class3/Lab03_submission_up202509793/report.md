# Lab03 - Network Scanning

## Ex01 - Banner grabbing

For this exercise I chose to further analyse the domain `flashpaper-dev3.chime.com`, a subdomain I started looking at in the previous lab. The name suggests a proprietary tool (`flashpaper`) and a development environment (`dev3`), which makes it interesting from a bug-hunting point of view.

The Chime Bugcrowd program scope states (paraphrased): **All Chime-owned assets and services are in scope, including development environments**, unless explicitly listed as out-of-scope. Because `flashpaper-dev3.chime.com` is not in the out-of-scope list, I consider it in-scope, but I will remain conservative and low-noise with active testing.

I planned to banner-grab a few common services and ports:
- HTTP(S) — 80 / 443
- SSH — 22
- SMTP — 25 (or submission 587)
- FTP — 21

Below are the results, interpretation and next steps.

**Important Note:** I already saw from the previous lab that this domain is protected by cloudflare. However, after some tests, I was able to confirm that so are all the other chime subdomains, so I will keep this one, even tho the results might not be very interesting.

---

### HTTP(S) banner grabbing

**Command used**
```bash
# quick header only (low noise)
curl -I -L --max-time 10 https://flashpaper-dev3.chime.com/
```

**Observed output (important headers)**
```
HTTP/2 404
content-type: text/plain; charset=utf-8
content-length: 19
cf-ray: 98a6c65dd9f75bda-LIS
x-router-sha: e40978b15b463099edbc3fc755395827de55758a
strict-transport-security: max-age=31622400; includeSubDomains; preload
content-security-policy: ...
cf-cache-status: DYNAMIC
set-cookie: __cf_bm=...
server: cloudflare
```

**Interpretation**
- The response was returned by **Cloudflare** (header `server: cloudflare`, `cf-ray`, etc.). Cloudflare is terminating TLS and acting as a reverse proxy/WAF/CDN.  
- Because the edge is handling TLS and responding, **it is not possible to see the origin server banners** (e.g., `Apache/2.4`, `nginx`, `OpenSSL` strings) from a straight `curl`.

---

### SSH banner grabbing

**Command used**
```bash
nc -v -w 3 flashpaper-dev3.chime.com 22
```

**Observed output**
```
nc: connect to flashpaper-dev3.chime.com (172.64.152.131) port 22 (tcp) timed out: Operation now in progress
nc: connect to flashpaper-dev3.chime.com (104.18.35.125) port 22 (tcp) timed out: Operation now in progress
```

**What this means**
- The TCP SYN did **not** get a SYN/ACK or an immediate RST → **timeout**. That usually indicates the packet was dropped/filtered (no response).  
- Cloudflare edge IPs generally **do not proxy SSH (port 22)** for standard plans. To proxy arbitrary TCP (SSH) you need Cloudflare Spectrum (Enterprise).
- As a result, it’s almost certain that Cloudflare is dropping the connection. Whether or not the origin server actually runs SSH cannot be determined from this test. Either way, trying to probe SSH on this hostname is a dead end.

---

### SMTP banner grabbing

**What I ran**
```bash
nc -w 5 flashpaper-dev3.chime.com 25
# then typed: EHLO example.com
```

**Observed behaviour**
- `nc` returned immediately (no banner), and when I typed `EHLO example.com` on my shell later, the shell responded `EHLO: command not found`.  
  That happened because the `nc` session had already closed (there was no SMTP banner and you were back to your shell), so `EHLO ...` was executed as a shell command.

**Interpretation**
- No SMTP service responded on port 25 through the Cloudflare edge (the connection was dropped/timed out silently). Cloudflare does not proxy SMTP on standard configurations, so this result is expected.  
- If an SMTP server were present and reachable, a `220` banner would be seen and then the `EHLO` exchange.

---

### FTP banner grabbing

**What I ran**
```bash
nc -w 5 flashpaper-dev3.chime.com 21
```

**Observed behaviour**
- No banner or response; `nc` returned immediately to prompt.

**Interpretation**
- Port 21 is filtered/closed from the public edge (again, Cloudflare will not proxy FTP). No FTP banner available via the public hostname.

---

### Summary of network-level results
- HTTP(S) responded, but the banner is Cloudflare’s. Origin server details (OS, web server version) are not visible via normal banner grabs.  
- Non-HTTP ports (22, 21, 25) are filtered/dropped at the edge — timeouts/no banners. This is expected with Cloudflare in front.  
- **Conclusion:** network/banner enumeration has reached its practical limit for this host. **Actionable testing remains at the application layer** (HTTP endpoints, APIs, JS, cookies, CSP/CORS). Network banner grabbing beyond Cloudflare’s allowed ports will be blocked or dropped.

---

## Ex02 - Exploring NMAP

For this second exercise I will be opting to use the IP provided by the professor. This is because, as seen before, all chime.com subdomains are fronted by Cloudflare reverse proxy, so `Nmap` would mostly talk to Cloudflare edges, hide the origin, and may even produce misleading results.

--- 

### Ex02.1 - How to perform a ping scan?

A ping scan lists if a host is up (doesn’t scan ports). \
To do it using `Nmap`, we can simply use the `-sn` tag.

**Command used**
```bash
sudo nmap -sn 100.101.159.45
```

**Observed output**
```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-10-06 19:50 WEST
Nmap scan report for tpas-be.tail9b2a2.ts.net (100.101.159.45)
Host is up (0.090s latency).
Nmap done: 1 IP address (1 host up) scanned in 0.09 seconds
```
**Interpretation** \
As seen by the third line of the output, the *Host is up*.

---

### Ex02.2 - How to perform an aggressive scan? What information can we get?

An aggresive scan is a scan that does:
 - OS detection; 
 - Version detection;
 - Script scanning;
 - Traceroute;
 
To do it, we can simply use the `-A` tag.

**Command used**
```bash
sudo nmap -A 100.101.159.45
```

**Observed output**
```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-10-06 23:12 WEST
Nmap scan report for tpas-be.tail9b2a2.ts.net (100.101.159.45)
Host is up (0.017s latency).
Not shown: 991 closed tcp ports (conn-refused)
PORT     STATE SERVICE          VERSION
22/tcp   open  ssh              OpenSSH 8.9p1 Ubuntu 3ubuntu0.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 fb:ad:d2:7b:62:da:fd:cb:75:d9:73:86:35:63:22:08 (ECDSA)
|_  256 55:4a:cc:f4:7e:3b:ca:cd:8b:99:7c:66:a8:12:82:8b (ED25519)
80/tcp   open  http             nginx 1.29.1
|_http-title: Did not follow redirect to https://tpas-be.tail9b2a2.ts.net/
|_http-server-header: nginx/1.29.1
443/tcp  open  ssl/http         nginx 1.29.1
|_http-server-header: nginx/1.29.1
| tls-alpn: 
|   http/1.1
|   http/1.0
|_  http/0.9
|_http-title: TPAS 2025/2026
| http-robots.txt: 1 disallowed entry 
|_/admin
| ssl-cert: Subject: commonName=tpas-desafios.alunos.dcc.fc.up.pt/organizationName=Universidade do Porto/stateOrProvinceName=Porto/countryName=PT
| Subject Alternative Name: DNS:tpas-desafios.alunos.dcc.fc.up.pt, DNS:www.tpas-desafios.alunos.dcc.fc.up.pt
| Not valid before: 2024-08-04T00:00:00
|_Not valid after:  2025-08-04T23:59:59
|_ssl-date: TLS randomness does not represent time
6002/tcp open  X11:2?
| fingerprint-strings: 
  (...)
6003/tcp open  http             Apache httpd 2.4.52 ((Debian))
|_http-server-header: Apache/2.4.52 (Debian)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
6004/tcp open  http             Apache httpd 2.4.54 ((Debian))
|_http-title: IP Service
|_http-server-header: Apache/2.4.54 (Debian)
6005/tcp open  X11:5?
| fingerprint-strings: 
  (...)
7000/tcp open  afs3-fileserver?
|_irc-info: Unable to open connection
| fingerprint-strings: 
  (...)
7001/tcp open  afs3-callback?
| fingerprint-strings: 
  (...)

TRACEROUTE
HOP RTT      ADDRESS
1   14.89 ms tpas-be.tail9b2a2.ts.net (100.101.159.45)
```

**Interpretation** \
As expected, the aggresive scan took some time but gave a lot of information, including:
 - Open ports
 - Services running
 - Versions and details of the services
 - Traceroute (It shows a single hop since I am dirrectly connected to the target because of the tailscale VPN)

Below is a summary of the findings:

| Port | State | Service | Version / Details | Key Findings & Potential Significance |
| :--- | :--- | :--- | :--- | :--- |
| **22/tcp** | Open | SSH | OpenSSH 8.9p1 Ubuntu | **Secure Shell access.** Standard for remote administration. The version suggests an Ubuntu system. |
| **80/tcp** | Open | HTTP | nginx 1.29.1 | **Main HTTP site.** It redirects to HTTPS (port 443). |
| **443/tcp** | Open | HTTPS | nginx 1.29.1 | **Main secure web application (TPAS 2025/2026).** The SSL cert is for `tpas-desafios.alunos.dcc.fc.up.pt`. A `robots.txt` file disallows access to `/admin`. |
| **6002/tcp** | Open | HTTP | gunicorn (Python) | **"My Files" Application.** A simple web app that lets you view text files (`quotes.txt`, `todo.txt`) via a `file` parameter (e.g., `/view?file=quotes.txt`). This is a potential target for **Local File Inclusion (LFI)** attacks if not properly secured. |
| **6003/tcp** | Open | HTTP | Apache 2.4.52 (Debian) | **Unknown Service.** The page has no title and returns plain text. This is a service that needs further investigation with a web browser or tools like `curl`. |
| **6004/tcp** | Open | HTTP | Apache 2.4.54 (Debian) | **"IP Service".** The title suggests a service that might show your IP address or perform geo-IP lookups. |
| **6005/tcp** | Open | HTTP | gunicorn (Python) | **"NDA Service".** Hosts a Non-disclosure agreement. Like port 6002, it's a Python app that could have its own set of vulnerabilities. |
| **7000/tcp** | Open | HTTP | gunicorn (Python) | **"Lab 02 - Random target picker".** |
| **7001/tcp** | Open | HTTP | Unknown (likely a proxy) | **Redirect Service.** This service redirects all requests to `http://localhost/index.html`. It's not serving its own content but acting as a gateway or proxy. |

---

### Ex02.3 - How to perform a scan for a given port range? E.g. scanning all TCP ports between port 1 and 1000.

In `Nmap`, to do scaning of specific ports or ports in a given range, there is the `-p` flag. \
Examples of use:
 - Scanning only port 22: `nmap -p22 <ip>`
 - Scanning ports from 5000 to 7000: `nmap -p5000-7000 <ip>`

**In the specific case of 1 to 1000**

**Command used**
```bash
sudo nmap -p1-1000 100.101.159.45
```
---

### Ex02.4 - How to perform a list scan? For this task, it's recommended to scan your home network.

To perform a list scan, `nmap` has the flag `-sL`.

**Command used**
```bash
sudo nmap -sL 192.168.1.0/24
```

**Observed output**
```
Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-10-08 16:17 WEST
Nmap scan report for 192.168.1.0
Nmap scan report for 192.168.1.1
Nmap scan report for 192.168.1.2
...
Nmap scan report for OMEN.Home (192.168.1.74)
...
```

**Interpretation**

What does a list scan do?
- Nmap takes the network range you specify (here, 256 addresses from .0 to .255),
- It resolves each IP’s hostname (using DNS or reverse DNS lookups),
- Then it simply prints the list of targets it would scan, but it does not send any packets to those hosts.

From my output we see most IPs did not resolve to hostnames, but some addresses that are registered in the local network (via the router/DHCP, mDNS, or reverse DNS) were resolved. For example 192.168.1.74 resolved to OMEN.Home, which is my HP OMEN laptop.

**Important note**

A list scan is very low-noise because it does not send probe packets to the targets, but it may still perform DNS queries to resolve names.

---

## Ex03 - Which scan made more noise? Using wireshark to find out.

### 1. Ping Scan (using Nmap -sn)

Command: `sudo nmap -sn 100.101.159.45` \
Wireshark Filters: `ip.addr == 192.168.1.74  && !ip.addr==192.200.0.101 && udp.port != 41641`

A simple ping command should only create 2 packets, ICMP request and ICMP reply. That is also what I expected for this command. However, when I ran this command, I was suprised to see about **60 packets** show up. Those included `UDP`, `TCP`, `ICMP`, `TLSv1.2` and `WireGuard Protocol`.

From a quick search, I was able to determine that:
 - `ICMP` is because of the classic ping behaviour;
 - `TCP` is because of SYN probes to 80/443 for host discovery;
 - `UDP` is because Nmap sometimes tests UDP ports or gets broadcast replies;
 - `TLSv1.2` is probably HTTPS replies or unrelated traffic;
 - `WireGuard` is background VPN traffic (from tailscale), also unrelated. I will be filtering it out in the next experiments;

---

### 2. Aggressive Scan (using Nmap -A)

Command: `sudo nmap -A 100.101.159.45` \
Wireshark Filters: `ip.addr == 192.168.1.74  && !ip.addr==192.200.0.101 && udp.port != 41641`

As expected, this scan created a lot of packets, however, because of the time it took, it is higly probable that unrelated packets appear, so the precise number of packets the scan itself takes is difficult to measure.

- **Number of Packets (Counting WireGuard):** ~5700 packets.
- **Number of Packets (NOT counting WireGuard):** ~587 packets.

**Conclusion** 

Excluding the extra VPN packets, the number of packets the scan requires drops by a lot. Still, almost 600 packets needed makes it quite the noisy scan.

---

### 3. Port range Scan (using Nmap -p)

Command: `sudo nmap -p1-1000 100.101.159.45` \
Wireshark Filters: `ip.addr == 192.168.1.74  && !ip.addr==192.200.0.101 && udp.port != 41641`

- **Number of Packets (Counting WireGuard):** ~1415 packets.
- **Number of Packets (NOT counting WireGuard):** ~128 packets.

---

### 4. List Scan (using Nmap -sL)

Command: `sudo nmap -sL 192.168.1.0/24` \
Wireshark Filters: `ip.addr == 192.168.1.74  && !ip.addr==192.200.0.101 && udp.port != 41641`

- **Number of Packets (NOT counting WireGuard):** ~570 packets.

**Note:** For this scan, all packets were DNS packets, as expected.

---

### Final conclusion

Final Ranking of the noisiest scans:

1. `Aggressive Scan` --> ~587 packets
2. `List Scan` --> ~570 packets (Potencial to be number 1, depending on the network size)
3. `Port range Scan` --> ~128 packets (Higly depends on the number of ports being scanned)
4. `Ping Scan` --> ~60 packets (By far the quietest, but makes a suprising amount of noise for a simple ping scan)

---

## Ex05 - Optional Exercises

## Ex05.1 - Banner grabbing and nmap scanning on other hosts from Lab 02 - subs.txt

to be done...

---

## Ex05.2 - Using scapy to extract all IPs from a pcapng file. 

First I created the python script `scapy_extract_ip.py`. Then I tested by creating a pcapng file (quick wireshark scan of the network) and using the script on it.

**Command used**
```bash
sudo python3 scapy_extract_ips.py quick_packets.pcapng 
```

**Observed output**
```
Extracted 5 unique IP addresses:

10.93.74.126
13.89.179.9
142.250.201.14
172.64.146.215
74.125.250.240
```

---

## Ex05.3 - Using scapy to do a SYN port scan on a given IP.

First I created the python script `scapy_syn_scan.py`. Then I tested by scanning the ports 6000 to 7000 of the TPAS IP.

**Command(s) used**
```bash
# For more information
sudo python3 scapy_syn_scan.py 100.101.159.45 --ports 6000-7000 --timeout 0.01 --rate 200

# To hide "filtered" outputs (less text bloat on the terminal)
sudo python3 scapy_syn_scan.py 100.101.159.45 --ports 6000-7000 --hide-filtered --timeout 0.01 --rate 200
```

**Observed output**
```
Scan complete.
Open ports (0): []
```

**Interpretation**

It is obviously not working, as we know from the `Nmap` scans that some ports are open in this range. However, I couldn't solve the issue in time for delivery. =(

