from src.tools import JobSearchTool
import json

tool = JobSearchTool()
# Use a query that likely has ads to test filtering
query = 'Associate Product Manager India' 
print("Running search with NEW logic...")
result = tool._run(query)
print("Processed Output:")
print(result)
