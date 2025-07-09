# test/zap_scan_test.py

from crewai import Task
from agents.pentest_agent import zap_recon_agent
from tools.zap_tool import OWASPZAPTool
from crewai import Crew
import os
from dotenv import load_dotenv


# Load environment variables from the .env.dev file
load_dotenv(dotenv_path=".env.dev")

# Set OpenAI credentials
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
os.environ["OPENAI_API_BASE"] = os.getenv("OPENAI_API_BASE_URL")

# ✅ Define the task
zap_task = Task(
    description="Scan the given web target using OWASP ZAP and return any vulnerabilities.",
    expected_output="List of vulnerabilities or confirmation that no issues were found.",
    agent=zap_recon_agent
)
zap_task.context = {"target": "http://localhost:3000/rest/user/whoami"}
  # ✅ Example URL, replace with actual target
# ✅ Run the test
if __name__ == "__main__":
    print("[🧪 Running ZAP test task...]")
    print(f"[🔗 ZAP Target URL]: {zap_task.context}")

    web_crew = Crew(
        agents=[zap_task.agent],
        tasks=[zap_task],
        verbose=True
    )
    zap_result = web_crew.kickoff()
    print("\n[🛡️ OWASP ZAP Output]:\n", zap_result)
