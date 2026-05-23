#!/usr/bin/env python3
"""
SubBrute: A fast subdomain enumeration tool using brute-force with a wordlist.
"""

import argparse
import concurrent.futures
import socket
import sys
from dns import resolver, exception

def resolve_subdomain(subdomain, domain, timeout=5):
    """
    Attempt to resolve a subdomain to an IP address.
    Returns the subdomain and IP if successful, otherwise None.
    """
    fqdn = f"{subdomain}.{domain}"
    try:
        answers = resolver.resolve(fqdn, 'A', lifetime=timeout)
        for rdata in answers:
            return fqdn, rdata.address
    except (exception.DNSException, socket.timeout):
        pass
    return None

def main():
    parser = argparse.ArgumentParser(description="Brute-force subdomain enumeration.")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Number of concurrent threads (default: 50)")
    parser.add_argument("--timeout", type=int, default=5, help="DNS query timeout in seconds (default: 5)")
    args = parser.parse_args()

    try:
        with open(args.wordlist, 'r') as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: Wordlist file '{args.wordlist}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading wordlist: {e}")
        sys.exit(1)

    print(f"[+] Starting subdomain enumeration for {args.domain}")
    print(f"[+] Using wordlist: {args.wordlist} ({len(subdomains)} entries)")
    print(f"[+] Threads: {args.threads}, Timeout: {args.timeout}s\n")

    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        future_to_subdomain = {
            executor.submit(resolve_subdomain, sub, args.domain, args.timeout): sub
            for sub in subdomains
        }
        for future in concurrent.futures.as_completed(future_to_subdomain):
            result = future.result()
            if result:
                fqdn, ip = result
                print(f"[+] Found: {fqdn} -> {ip}")
                found.append((fqdn, ip))

    print(f"\n[+] Enumeration complete. Found {len(found)} subdomains.")
    if found:
        print("[+] Results:")
        for fqdn, ip in found:
            print(f"    {fqdn} -> {ip}")

if __name__ == "__main__":
    main()