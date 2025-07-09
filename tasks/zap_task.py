from crewai import Task
from agents.pentest_agent import zap_recon_agent
from tools.zap_tool import OWASPZAPTool

zap_task = Task(
    description="Scan the given web target {target} using OWASP ZAP and return any vulnerabilities.",
    expected_output="A list of vulnerabilities found by OWASP ZAP or a clean report.",
    agent=zap_recon_agent
    #tools=[OWASPZAPTool()]
)



