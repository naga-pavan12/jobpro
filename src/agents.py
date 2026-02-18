from crewai import Agent, LLM
from src.tools import JobSearchTool

class JobAgents:
    def __init__(self):
        # We assume Ollama is running locally on default port 11434
        self.llm = LLM(
            model="ollama/llama3.2:latest", 
            base_url="http://localhost:11434"
        )

    def job_scout_agent(self):
        return Agent(
            role="Senior Technical Recruiter",
            goal="Find active job postings matching the user's criteria.",
            backstory=(
                "You are an elite headhunter. You hate 'ghost jobs' and vague descriptions. "
                "You only select roles that are active and strictly match requirements."
            ),
            tools=[JobSearchTool()],
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )

    def resume_strategist_agent(self):
        return Agent(
            role="ATS Optimization Specialist",
            goal="Tailor the resume summary and skills to match the best found job.",
            backstory=(
                "You are an expert at beating Applicant Tracking Systems (ATS). "
                "You mirror keywords from the JD into the resume without fabricating experience. "
                "You value truth and impact."
            ),
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )

    def outreach_specialist_agent(self):
        return Agent(
            role="Corporate Communications Manager",
            goal="Draft a professional cold email for the job application.",
            backstory=(
                "You write emails that get opened. "
                "You avoid generic fluff like 'To whom it may concern'. "
                "You focus on value, brevity, and a clear call to action."
            ),
            verbose=True,
            llm=self.llm,
            allow_delegation=False
        )
