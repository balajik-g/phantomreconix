import subprocess
import os

class NmapScanner:
    def __init__(self, output_dir="logs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def scan(self, target):
        print(f"[+] Running Nmap scan on: {target}")
        output_file = os.path.join(self.output_dir, f"{target}_nmap.txt")

        try:
            result = subprocess.run([
                "nmap", "-Pn", "-sS", "-T4", "-p", "1-1000",
                target, "-oN", output_file
            ], capture_output=True, text=True)

            if result.returncode != 0:
                print(f"[!] Nmap error:\n{result.stderr}")
                return None

            with open(output_file, "r") as f:
                scan_output = f.read()
            return scan_output

        except Exception as e:
            print(f"[!] Exception running Nmap: {e}")
            return None

# Exposed function
def run_nmap_scan(target):
    scanner = NmapScanner()
    return scanner.scan(target)
