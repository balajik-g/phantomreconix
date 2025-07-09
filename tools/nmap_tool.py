## nmap_tool.py
from crewai.tools import BaseTool
import subprocess
import os
import re

class NmapScanTool(BaseTool):
    name: str = "Nmap Port Scanner"
    description: str = "Scans the target for open ports using Nmap."

    def sanitize_filename(self, target: str) -> str:
        # Replace all non-alphanumeric characters with underscores
        return re.sub(r"[^\w]", "_", target)

    def _run(self, target: str) -> str:
        print("DEBUG INPUT", target)
        safe_target = self.sanitize_filename(target)

        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)

        # Build output file path
        output_file = os.path.join("logs", f"{safe_target}_nmap.txt")

        # Build Nmap command
        cmd = ["nmap", "-Pn", "-sS", "-T4", "-p", "1-1000", "-oN", output_file, target]

        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error during Nmap scan:\n{e.output}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
