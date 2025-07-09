# main.py
import os
import re
from dotenv import load_dotenv
from crewai import Crew

from tasks.nmap_task import nmap_task
from tasks.zap_task import zap_task
from tasks.api_enum_task import api_enum_task  # NEW

# Load environment variables from the .env.dev file
load_dotenv(dotenv_path=".env.dev")

# Set OpenAI credentials
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE_URL")

if __name__ == "__main__":
    target = input("Enter the target IP or URL: ").strip()

    # Set target for Nmap
    nmap_task.context = target

    # -------------------------------
    # Step 1: Run Nmap
    crew = Crew(
        agents=[nmap_task.agent],
        tasks=[nmap_task],
        verbose=True
    )
    #nmap_result = crew.kickoff()
    nmap_result = crew.kickoff(inputs={"target": target})
    print("\n🧾 Nmap Output:\n", nmap_result)

    nmap_result_str = str(nmap_result)

    # -------------------------------
    # Step 2: Run ZAP if web ports found
    if re.search(r"80/tcp.*http", nmap_result_str) or re.search(r"443/tcp.*https", nmap_result_str):
        print("\n[🌐 Web ports detected! Initiating OWASP ZAP scan...]")

        # Normalize URL for ZAP
        if target.__contains__("example.com"):
            print("[❗] Invalid target. Please provide a valid URL.")
            exit(1)

        zap_url = f"http://{target}" if not target.startswith("http") else target
        zap_task.context = {"target": zap_url}
        print(f"[🔗 ZAP Target URL]: {zap_task.context}")

        web_crew = Crew(
            agents=[zap_task.agent],
            tasks=[zap_task],
            verbose=True
        )
        zap_result = web_crew.kickoff(inputs={"target": target})
        print("\n[🛡️ OWASP ZAP Output]:\n", zap_result)

        # -------------------------------
        # Step 3: Run API Enumeration (if relevant)
    if any(keyword in target.lower() for keyword in ["api", "graphql"]) or re.search(r"/api|/graphql", target, re.IGNORECASE):
        print("\n[🔍 Detected API keyword, starting API Enumeration...]")
        api_enum_task.context = target
        api_crew = Crew(
        agents=[api_enum_task.agent],
        tasks=[api_enum_task],
        verbose=True
        )
        api_enum_result = api_crew.kickoff(inputs={"target": target})
        print("\n[🔎 API Enumeration Output]:\n", api_enum_result)
    else:
        print("\n[✅ No API pattern detected in URL. Skipping API Enumeration.]")
else:
    print("\n[✅ No web ports found. OWASP ZAP and API Enumeration skipped.]")
