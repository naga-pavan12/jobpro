import requests
from bs4 import BeautifulSoup
import json

def ddg_search(query, max_results=10):
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    # Refine query for jobs
    search_query = f"{query} jobs hiring now"
    data = {"q": search_query, "df": "w"}
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    
    for result in soup.find_all('div', class_='result'):
        title_tag = result.find('a', class_='result__a')
        snippet_tag = result.find('a', class_='result__snippet')
        
        if title_tag:
            link = title_tag.get('href')
            title = title_tag.get_text(strip=True)
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else "No description"
            
            if link and title:
                results.append({
                    "title": title,
                    "link": link,
                    "description": snippet
                })
                if len(results) >= max_results:
                    break
                    
    return results

print(json.dumps(ddg_search("Python Developer jobs"), indent=2))
