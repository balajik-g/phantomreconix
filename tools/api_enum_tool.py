#api_enum_tool.py
rom crewai.tools import BaseTool
import requests

class APIEnumeratorTool(BaseTool):
    name: str = "API Enumerator"
    description: str = "Discovers APIs (REST/GraphQL) on the target domain using common paths."

    def _run(self, target: str) -> str:
        api_paths = ["/api", "/api/v1", "/api/v2", "/graphql", "/rest", "/swagger", "/openapi.json"]
        discovered = []

        for path in api_paths:
            url = f"{target.rstrip('/')}{path}"
            try:
                response = requests.get(url, timeout=5)
                if response.status_code in [200, 401, 403]:
                    discovered.append(url)
            except Exception:
                continue

        if discovered:
            return "Discovered API endpoints:\n" + "\n".join(discovered)
        else:
            return "No common API endpoints found."
