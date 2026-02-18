from crewai import Crew, Process
from src.agents import JobAgents
from src.tasks import JobTasks

class JobHunterCrew:
    def __init__(self, job_role, location, experience_level, resume_content):
        self.job_role = job_role
        self.location = location
        self.experience_level = experience_level
        self.resume_content = resume_content
        
    def run(self):
        # Initialize Agents
        agents = JobAgents()
        scout = agents.job_scout_agent()
        strategist = agents.resume_strategist_agent()
        outreach = agents.outreach_specialist_agent()
        
        # Initialize Tasks
        tasks = JobTasks()
        
        # Explicitly passing context/data where needed
        criteria = f"Job Role: {self.job_role}, Location: {self.location}, Experience Level: {self.experience_level}"
        
        search_task = tasks.search_task(scout, criteria)
        
        # Note: The 'jobs' argument in tailor_task definition is primarily for the description string,
        # but the actual data flow in CrewAI relies on the 'context' parameter or pure sequential execution
        # passing the output of the previous task. 
        # Here we rely on CrewAI's context passing mechanism via the `context` parameter in Task definition.
        
        tailor_task = tasks.tailor_task(strategist, self.resume_content, [search_task])
        outreach_task = tasks.outreach_task(outreach, [tailor_task], [search_task])
        
        # Form the Crew
        crew = Crew(
            agents=[scout, strategist, outreach],
            tasks=[search_task, tailor_task, outreach_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Kickoff
        result = crew.kickoff()
        return result
