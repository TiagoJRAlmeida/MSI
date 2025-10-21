#!/usr/bin/env python3
"""
scapy_syn_scan.py
Simple TCP SYN port scanner using Scapy.

Requirements:
    sudo pip install scapy

Usage:
    sudo python3 scapy_syn_scan.py target --ports 1-1024,8080 --timeout 1 --rate 200

Warning: Only scan hosts you own or have explicit permission to test.
"""

import argparse
import socket
import time
from typing import List, Tuple

from scapy.all import IP, TCP, sr1, RandShort, conf

# Reduce scapy verbose output
conf.verb = 0


# Parse port specifications like "22,80,443,8000-8100" into a sorted unique list of ints.
def parse_ports(ports_str: str) -> List[int]:
    
    ports = set()
    parts = ports_str.split(',')
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if '-' in p:
            a, b = p.split('-', 1)
            a, b = int(a), int(b)
            if a > b:
                a, b = b, a
            for port in range(a, b + 1):
                ports.add(port)
        else:
            ports.add(int(p))
    return sorted(ports)


# Send a TCP SYN to target_ip:port. Return tuple (ip, port, status) where status in {"open","closed","filtered"}.
def scan_port(target_ip: str, port: int, timeout: float) -> Tuple[str, int, str]:

    # craft packet
    src_port = RandShort()
    pkt = IP(dst=target_ip)/TCP(sport=src_port, dport=port, flags="S")
    try:
        resp = sr1(pkt, timeout=timeout)
    except PermissionError as e:
        raise
    if resp is None:
        return (target_ip, port, "filtered")  # no response (filtered/drop)
    # If there's a TCP layer in response
    if resp.haslayer(TCP):
        tcp_layer = resp.getlayer(TCP)
        flags = tcp_layer.flags
        # SYN-ACK -> open
        if flags == 0x12 or ('S' in str(flags) and 'A' in str(flags)):  # 0x12 = SYN+ACK
            # send RST to close handshake politely
            rst = IP(dst=target_ip)/TCP(sport=src_port, dport=port, flags="R")
            try:
                sr1(rst, timeout=0.5)
            except Exception:
                pass
            return (target_ip, port, "open")
        # RST (or RST-ACK) -> closed
        elif flags & 0x14:  # RST (0x04) or RST+ACK(0x14)
            return (target_ip, port, "closed")
    # other unusual responses -> filtered/unknown
    return (target_ip, port, "filtered")

def main():
    parser = argparse.ArgumentParser(description="SYN port scanner using Scapy. Use only on permitted targets.")
    parser.add_argument("target", help="IP or hostname to scan")
    parser.add_argument("--ports", default="1-1024", help="Ports to scan. Examples: '22,80,443' or '1-1024,8080'. Default: 1-1024")
    parser.add_argument("--timeout", type=float, default=1.0, help="Timeout (seconds) waiting for replies per probe. Default: 1.0")
    parser.add_argument("--rate", type=float, default=100.0, help="Approx probes per second (simple throttle). Default: 100")
    parser.add_argument("--hide-filtered", action="store_true", help="Do not show ports whose status is 'filtered'.")
    args = parser.parse_args()

    # Resolve target
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"ERROR: Could not resolve hostname: {args.target}")
        return

    # Build port list
    try:
        ports = parse_ports(args.ports)
    except Exception as e:
        print(f"ERROR parsing ports: {e}")
        return

    if args.rate <= 0:
        delay_between = 0.0
    else:
        delay_between = 1.0 / args.rate

    print(f"Scanning {args.target} ({target_ip})")
    print(f"Ports: {len(ports)} ports (first 10 shown): {ports[:10]}{'...' if len(ports)>10 else ''}")
    print(f"Timeout per probe: {args.timeout}s, Rate: {args.rate} probes/s, delay={delay_between:.4f}s\n")

    results = []
    try:
        for i, port in enumerate(ports, start=1):
            try:
                ip, p, status = scan_port(target_ip, port, timeout=args.timeout)
            except PermissionError:
                print("PermissionError: Raw sockets require root/administrator privileges. Run with sudo / as admin.")
                return
            except Exception as e:
                status = f"error: {e}"
            results.append((ip, p, status))

            is_filtered = isinstance(status, str) and "filtered" in status.lower()
            if args.hide_filtered and is_filtered:
                # skip printing filtered results
                pass
            else:
                print(f"[{i}/{len(ports)}] {p:5d} -> {status}")
            
            if delay_between > 0:
                time.sleep(delay_between)
    except KeyboardInterrupt:
        print("\nScan interrupted by user. Reporting results so far...\n")

    # Summary
    open_ports = [p for (ip,p,s) in results if s == "open"]
    print("\nScan complete.")
    print(f"Open ports ({len(open_ports)}): {sorted(open_ports)}")

if __name__ == "__main__":
    main()
