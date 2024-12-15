import requests
import time
import json
import os
import sys

NAMECHEAP_API_URL = "https://dynamicdns.park-your-domain.com/update"
DOMAIN = os.getenv('DOMAIN')
SUBDOMAINS = os.getenv('SUBDOMAINS', '').split(',')
DYNAMIC_DNS_PASSWORD = os.getenv('DYNAMIC_DNS_PASSWORD')
CHECK_INTERVAL_SECONDS = int(os.getenv('CHECK_INTERVAL_SECONDS', 1800))

def get_public_ip():
    try:
        ip = requests.get('https://api.ipify.org').text.strip()
        print(f"[DynDNS] Fetched public IP: {ip}")
        return ip
    except requests.RequestException:
        print("[DynDNS] Error getting public IP address")
        return None

def update_dns_record(subdomain, ip):
    url = f"{NAMECHEAP_API_URL}?host={subdomain}&domain={DOMAIN}&password={DYNAMIC_DNS_PASSWORD}&ip={ip}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"[DynDNS] DNS record for {subdomain}.{DOMAIN} updated to {ip}")
        else:
            print(f"[DynDNS] Error updating DNS record for {subdomain}.{DOMAIN}: {response.text}")
    except requests.RequestException as e:
        print(f"[DynDNS] Error making request to Namecheap: {e}")

def get_last_known_ip(filename='last_ip.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            ip = data.get('ip', '').strip()
            print(f"[DynDNS] Last known IP: {ip}")
            return ip
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def save_current_ip(ip, filename='last_ip.json'):
    with open(filename, 'w') as f:
        json.dump({'ip': ip}, f)

def main():
    if not DOMAIN or not DYNAMIC_DNS_PASSWORD or not SUBDOMAINS:
        print("[DynDNS] DOMAIN, DYNAMIC_DNS_PASSWORD, and SUBDOMAINS must be set")
        sys.exit(1)

    print("[DynDNS] Starting DNS update script...")
    last_known_ip = get_last_known_ip()

    while True:
        current_ip = get_public_ip()

        if current_ip:
            if current_ip != last_known_ip:
                print(f"[DynDNS] IP address has changed: {current_ip}")
                for subdomain in SUBDOMAINS:
                    update_dns_record(subdomain, current_ip)

                save_current_ip(current_ip, 'last_ip.json')
                last_known_ip = current_ip
        else:
            print("[DynDNS] Could not retrieve public IP address, retrying in 30 seconds.")

        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == '__main__':
    main()
