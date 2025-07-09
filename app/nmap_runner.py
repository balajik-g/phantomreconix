# app/nmap_runner.py

# app/nmap_runner.py

import subprocess

def run_nmap_scan(target: str) -> str:
    try:
        result = subprocess.check_output(["nmap", "-sV", target], stderr=subprocess.STDOUT, text=True, timeout=60)
        return result
    except subprocess.CalledProcessError as e:
        return f"[!] Error running Nmap: {e.output}"
    except Exception as e:
        return f"[!] Unexpected error: {str(e)}"

