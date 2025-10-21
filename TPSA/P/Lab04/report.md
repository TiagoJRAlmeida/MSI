# Lab04

## Ex01 - Zone transfer on the up.pt domain

### Step 1 - Find the Name Servers for the domain

To find the nameservers related to a given domain, we can we either the whois command

```bash
# Command
whois up.pt | grep "Name Server"

# Output
Name Server: ns02.fccn.pt | IPv4: 193.136.2.228 and IPv6: 2001:690:a80:4001::200
Name Server: ns1.up.pt | IPv4: 193.137.55.30 and IPv6: 2001:690:2200:a10::30
Name Server: ns2.up.pt | IPv4: 193.137.55.31 and IPv6: 2001:690:2200:a10::31
Name Server: ns3.up.pt | IPv4: 193.137.55.32 and IPv6: 2001:690:2200:a10::32
Name Server: ns4.up.pt | IPv4: 193.137.55.33 and IPv6: 2001:690:2200:a10::33
```

Or use the `dig` tool, a tool created to interact with DNS servers.
With `dig`, we can query the DNS server to get the Name Servers linked to a respective domain.

```bash
# Command
dig +short NS up.pt

# Output
ns1.up.pt.
ns4.up.pt.
ns02.fccn.pt.
ns3.up.pt.
ns2.up.pt.
```

**Conclusion**

The domain up.pt has 5 name servers. I need to choose one to do the zone transfer attack so I will continue with `ns1.up.pt`.

### Step 2 - Do the Zone Transfer attack

To do a zone transfer attack there are many tools. I will be using dig.

**Command**

```bash
dig @ns1.up.pt up.pt axfr
```

**Output**

```bash
; <<>> DiG 9.18.39-0ubuntu0.24.04.1-Ubuntu <<>> @ns1.up.pt up.pt axfr
; (2 servers found)
;; global options: +cmd
; Transfer failed.
```

**Conclusion**

As we saw, the Transfer failed, which means the Name server is properly configured and not vunerable to zone transfer attacks.


## Ex02

## Ex03

What we know:
    - Password hash: `FhFw5Pfw6kQEiSP4+tSkew5kdRzCdtqGaybFFRsPH1OA1oUYqkLdDSg6WzfRCoL3FN1pXyGq9OlE+1iYCUI0uFsG9FNFwls3`
    - Hashing Method: LDAP SHA512
    - Only lower case characters and digits
    - Password length: between 4 and 10

**Command**

```bash
echo '{SSHA512}FhFw5Pfw6kQEiSP4+tSkew5kdRzCdtqGaybFFRsPH1OA1oUYqkLdDSg6WzfRCoL3FN1pXyGq9OlE+1iYCUI0uFsG9FNFwls3' > hash.txt

# We don't know the password size, so we will try different sizes until we find one that outputs something
hashcat -a 3 -m 1711 -1 abcdefghijklmnopqrstuvwxyz0123456789 hash.txt ?1?1?1?1 --quiet
hashcat -a 3 -m 1711 -1 abcdefghijklmnopqrstuvwxyz0123456789 hash.txt ?1?1?1?1?1 --quiet
hashcat -a 3 -m 1711 -1 abcdefghijklmnopqrstuvwxyz0123456789 hash.txt ?1?1?1?1?1?1 --quiet

# Output
{SSHA512}FhFw5Pfw6kQEiSP4+tSkew5kdRzCdtqGaybFFRsPH1OA1oUYqkLdDSg6WzfRCoL3FN1pXyGq9OlE+1iYCUI0uFsG9FNFwls3:1jc37x
```

**Conclusion**

The password was `1jc37x` and so the flag is `TPAS{1jc37x}`.

## Ex04

### Step 1 - Find the version of Nginx Running

Using the following Nmap command

```bash
sudo nmap -sV -p7001 100.101.159.45
```