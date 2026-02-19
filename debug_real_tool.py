from src.tools import JobSearchTool
import json

def test_tool():
    tool = JobSearchTool()
    # Using the default values from app.py to reproduce the user's scenario
    job_role = "Python Developer"
    location = "Remote"
    experience = "1-3 Years"
    
    query = f"Job Role: {job_role}, Location: {location}, Experience Level: {experience}"
    print(f"Testing Tool with Query: {query}")
    
    try:
        result = tool._run(query)
        print("\nTool Output:")
        print(result)
        
        data = json.loads(result)
        if isinstance(data, list) and len(data) > 0:
            print(f"\nSuccess! Found {len(data)} jobs.")
            print("First job sample:", data[0])
        else:
            print("\nWarning: Tool returned empty list or error.")
            
    except Exception as e:
        print(f"\nError running tool: {e}")

if __name__ == "__main__":
    test_tool()
