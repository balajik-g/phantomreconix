from crewai.tools import BaseTool

class OWASPZAPTool(BaseTool):
    name: str = "OWASP ZAP Scanner"
    description: str = "Scans the target website for common web vulnerabilities using OWASP ZAP."

    def _run(self, target: str) -> str:
        from zapv2 import ZAPv2
        import time

        zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})

        try:
            # target contains example.com for testing purposes
            if "example.com" in target:
                raise ValueError("Invalid target URL for testing purposes. Please provide a valid URL.")
                            
            print(f"[+] Accessing target {target}")
            zap.urlopen(target)
            time.sleep(2)

            print(f"[+] Starting passive scan...")
            while int(zap.pscan.records_to_scan) > 0:
                print(f"[...] {zap.pscan.records_to_scan} records left")
                time.sleep(2)

            print(f"[+] Starting active scan...")
            scan_id = zap.ascan.scan(target)
            while int(zap.ascan.status(scan_id)) < 100:
                print(f"[...] Scan progress: {zap.ascan.status(scan_id)}%")
                time.sleep(5)

            alerts = zap.core.alerts(baseurl=target)
            output = f"[+] Scan complete. Found {len(alerts)} issues.\n"
            for alert in alerts:
                output += f"- {alert['alert']} ({alert['risk']}) on {alert['url']}\n"

            return output

        except Exception as e:
            return f"[!] ZAP Scan failed: {str(e)}"
