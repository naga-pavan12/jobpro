from crewai import Task
from src.models import JobSearchSchema, TailoredResume, EmailDraft
from src.tools import JobSearchTool

class JobTasks:
    def search_task(self, agent, criteria):
        return Task(
            description=(
                f"Search for job postings based on the following criteria: {criteria}. "
                "You MUST use the 'JobSearchTool' to retrieve real data. "
                "Do NOT generate fake jobs or use your training data. "
                "Return the exact list of jobs provided by the tool. "
                "IMPORTANT: You MUST include the 'link' field for every job. "
                "Use the exact URL provided by the tool. Do not modify or remove links."
            ),
            expected_output="A list of job postings in JSON format. Do not alter the tool output.",
            agent=agent,
            tools=[JobSearchTool()],
        )

    def tailor_task(self, agent, resume_content, jobs):
        return Task(
            description=(
                f"Analyze the User's Resume: '{resume_content}'. "
                "Compare it against the top job found in the search results: {jobs}. "
                "Rewrite the 'Summary' and 'Key Skills' sections to exactly match the keywords "
                "and requirements of that specific job description. "
                "Do NOT invent new skills, but rephrase existing ones to match the JD language."
            ),
            expected_output="A TailoredResume object with a refined summary, key skills, and experience bullets.",
            agent=agent,
            output_pydantic=TailoredResume,
            context=jobs # This task depends on the output of the search task
        )

    def outreach_task(self, agent, tailored_resume, job_details):
        return Task(
            description=(
                "Draft a high-conversion cold email to the hiring manager for the job we targeted. "
                "Use the tailored resume content to highlight why the candidate is a perfect fit. "
                "Keep it under 150 words. "
                "Catchy subject line."
            ),
            expected_output="An EmailDraft object containing the subject line and body.",
            agent=agent,
            output_pydantic=EmailDraft,
            context=tailored_resume # This task depends on the tailored resume
        )
