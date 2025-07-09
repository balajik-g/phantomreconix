import os
import subprocess
import json

def run_sublist3r(domain):
    print(f"[+] Running Sublist3r for: {domain}")
    output_file = f"logs/{domain}_subdomains.txt"
    os.makedirs("logs", exist_ok=True)

    subprocess.run([
        "sublist3r", "-d", domain, "-o", output_file
    ])

    if not os.path.exists(output_file):
        print(f"[!] Sublist3r failed — output file not found for {domain}")
        return []

    with open(output_file, "r") as f:
        raw_subdomains = f.read().splitlines()
    subdomains = [sub.strip() for sub in raw_subdomains if sub and "." in sub]

    return subdomains


def run_nmap_scan(target):
    print(f"[+] Scanning {target} for open ports...")
    output_file = f"logs/{target}_nmap.txt"
    os.makedirs("logs", exist_ok=True)

    try:
        subprocess.run([
            "nmap", "-Pn", "-sS", "-T4", "-p", "1-1000", target, "-oN", output_file
        ], check=True)
    except subprocess.CalledProcessError:
        print("[!] Nmap scan failed.")
        return "Nmap scan failed."

    with open(output_file, "r") as f:
        scan_result = f.read()

    return scan_result

def run_recon(target):
    subdomains = run_sublist3r(target)
    nmap_result = run_nmap_scan(target)

    return {
        "subdomains": subdomains,
        "nmap_scan": nmap_result
    }

if __name__ == "__main__":
    domain = input("Enter domain/IP for recon: ").strip()
    result = run_recon(domain)
    print(json.dumps(result, indent=2))
