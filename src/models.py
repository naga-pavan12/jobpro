from pydantic import BaseModel, Field
from typing import List

class JobPosting(BaseModel):
    title: str = Field(..., description="The job title")
    company: str = Field(..., description="The hiring company name")
    location: str = Field(..., description="Job location (e.g. Remote, City)")
    salary: str = Field(..., description="Salary range if available, else 'Competitive'")
    link: str = Field(..., description="Link to the job posting")
    description: str = Field(..., description="Brief summary of requirements")

class JobSearchSchema(BaseModel):
    jobs: List[JobPosting] = Field(..., description="List of found job postings")

class TailoredResume(BaseModel):
    summary: str = Field(..., description="Professional summary tailored to the job")
    key_skills: List[str] = Field(..., description="List of technical skills matching the JD")
    experience_bullets: List[str] = Field(..., description="Refined experience bullet points")

class EmailDraft(BaseModel):
    subject_line: str = Field(..., description="Catchy email subject line")
    email_body: str = Field(..., description="The main body content of the cold email")
