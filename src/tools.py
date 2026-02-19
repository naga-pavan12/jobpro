import json
import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool

class JobSearchTool(BaseTool):
    name: str = "JobSearchTool"
    description: str = "MANDATORY: Use this tool to search for real job listings. Input: a simple string query (e.g. 'Python Remote'). Output: JSON list of jobs."

    def _run(self, query: str) -> str:
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        
        # Refine query for jobs
        search_query = f"{query} jobs hiring now"
        # 'df': 'w' filters for results from the past week
        data = {"q": search_query, "df": "w"}
        
        from urllib.parse import unquote
        
        results = []
        try:
            response = requests.post(url, data=data, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            for result in soup.find_all('div', class_='result'):
                # Skip ads
                if 'result--ad' in result.get('class', []):
                    continue
                    
                title_tag = result.find('a', class_='result__a')
                snippet_tag = result.find('a', class_='result__snippet')
                
                if title_tag:
                    raw_link = title_tag.get('href')
                    title = title_tag.get_text(strip=True)
                    snippet = snippet_tag.get_text(strip=True) if snippet_tag else "No description"
                    
                    if raw_link and title:
                        link = raw_link
                        # Decode DDG redirect if present
                        if 'uddg=' in raw_link:
                            try:
                                # Extract url from /l/?kh=-1&uddg=HTTPS_URL
                                from urllib.parse import parse_qs, urlparse
                                parsed = urlparse(raw_link)
                                query_params = parse_qs(parsed.query)
                                if 'uddg' in query_params:
                                    link = query_params['uddg'][0]
                            except:
                                pass # Use raw link if decoding fails
                        
                        # Skip ad tracking links (y.js) if they slipped through class check
                        if 'y.js' in link or 'duckduckgo.com' in link:
                             # Try to see if it's a valid redirect we missed, otherwise generic skip
                             pass

                        results.append({
                            "title": title,
                            "company": "See Link", 
                            "location": "See Link", 
                            "salary": "N/A", # Scraper doesn't easily get this from snippet
                            "link": link, 
                            "description": snippet
                        })
                        
                if len(results) >= 20:
                    break
                    
        except Exception as e:
            return json.dumps([{"error": f"Search failed: {e}"}])

        if not results:
             return json.dumps([{"error": "No jobs found. Try a different query."}])
             
        return json.dumps(results, indent=2)
