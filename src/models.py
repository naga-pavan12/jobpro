from pydantic import BaseModel, Field
from typing import List, Optional

class JobPosting(BaseModel):
    title: Optional[str] = Field(default="N/A", description="The job title")
    company: Optional[str] = Field(default="N/A", description="The hiring company name")
    location: Optional[str] = Field(default="N/A", description="Job location (e.g. Remote, City)")
    salary: Optional[str] = Field(default="Competitive", description="Salary range if available, else 'Competitive'")
    link: Optional[str] = Field(default="#", description="Link to the job posting")
    description: Optional[str] = Field(default="No description available", description="Brief summary of requirements")

class JobSearchSchema(BaseModel):
    jobs: List[JobPosting] = Field(..., description="List of found job postings")

class TailoredResume(BaseModel):
    summary: str = Field(..., description="Professional summary tailored to the job")
    key_skills: List[str] = Field(..., description="List of technical skills matching the JD")
    experience_bullets: List[str] = Field(..., description="Refined experience bullet points")

class EmailDraft(BaseModel):
    subject_line: str = Field(..., description="Catchy email subject line")
    email_body: str = Field(..., description="The main body content of the cold email")
