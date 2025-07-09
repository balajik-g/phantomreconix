from crewai import Task
from agents.pentest_agent import api_enum_agent

api_enum_task = Task(
    description="Scan the target {target} to identify any exposed REST or GraphQL API endpoints.",
    expected_output="List of reachable API endpoints such as /api, /graphql, /swagger etc.",
    agent=api_enum_agent
)
