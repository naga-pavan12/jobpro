import json
from crewai.tools import BaseTool

class JobSearchTool(BaseTool):
    name: str = "JobSearchTool"
    description: str = "Useful to search for active job postings based on a query. Returns a list of jobs."

    def _run(self, query: str) -> str:
        from duckduckgo_search import DDGS
        
        results = []
        with DDGS() as ddgs:
            # Search for jobs specifically
            search_query = f"{query} jobs hiring now"
            # Getting more results to filter
            ddg_results = list(ddgs.text(search_query, max_results=60))
            
            for r in ddg_results:
                results.append({
                    "title": r.get('title', 'N/A'),
                    "company": "See Link", # DDG text search often puts company in title or body
                    "location": "See Link",
                    "salary": "N/A",
                    "link": r.get('href', 'N/A'),
                    "description": r.get('body', 'N/A')
                })

        if not results:
             return json.dumps([{"error": "No jobs found. Try a different query."}])
             
        return json.dumps(results, indent=2)
