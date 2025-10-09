from scapy.all import rdpcap, IP
import sys

def extract_ip_addresses(pcap_file):
    
    # Read the capture file
    packets = rdpcap(pcap_file)

    ip_addresses = set()

    # Iterate through packets and collect IPs
    for pkt in packets:
        if IP in pkt:
            ip_addresses.add(pkt[IP].src)
            ip_addresses.add(pkt[IP].dst)

    return ip_addresses


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <file.pcapng>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    ips = extract_ip_addresses(pcap_file)

    print(f"\nExtracted {len(ips)} unique IP addresses:\n")
    for ip in sorted(ips):
        print(ip)
