from crewai import Task
from agents.pentest_agent import nmap_recon_agent

nmap_task = Task(
    description="Perform an Nmap scan on the target {target} and return a list of open ports and services.",
    expected_output="A list of open ports with associated services, formatted in a readable way.",
    agent=nmap_recon_agent,
)
