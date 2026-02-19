from src.agents import JobAgents
from src.tasks import JobTasks
from crewai import Crew

def test_search_and_parse():
    agents = JobAgents()
    tasks = JobTasks()

    # Create the agent
    scout_agent = agents.job_scout_agent()
    
    # Create the task
    search_criteria = '{"job_role": "Associate Product Manager", "location": "India", "experience_level": "1-3 Years"}'
    search_task = tasks.search_task(scout_agent, search_criteria)

    # Create crew with just this task
    crew = Crew(
        agents=[scout_agent],
        tasks=[search_task],
        verbose=True
    )

    print("Starting Crew execution...")
    result = crew.kickoff()
    
    print("\n\n########################")
    print("FINAL OUTPUT:")
    print(result)
    print("########################\n")

    # Check the structured output if possible
    # crewai returns a CrewOutput object, we can inspect .pydantic or .json_dict if available
    # But usually .kickoff() returns the final result string/pydantic object depending on configuration.
    # In earlier logs, we saw it returning a Pydantic object wrapped in a TaskOutput.
    
    try:
        # access the output of the task
        task_output = search_task.output
        print("Task Output Pydantic:")
        print(task_output.pydantic)
    except Exception as e:
        print(f"Could not access Pydantic output: {e}")

if __name__ == "__main__":
    test_search_and_parse()
