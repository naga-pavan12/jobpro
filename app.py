import streamlit as st
import textwrap
import sys
import os
import io
import time
from src.crew import JobHunterCrew

# --- Page Config ---
st.set_page_config(
    page_title="JobHunter Pro",
    page_icon="💼",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    /* Modern AI Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
        color: #E6E6E6;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #12141C;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Inputs */
    .stTextInput input, .stTextArea textarea {
        background-color: #1D212E !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #4ECDC4 !important;
        box-shadow: 0 0 0 1px #4ECDC4 !important;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #FF6B6B 0%, #556270 100%);
        border: none;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4);
        color: white !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161B22;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        color: #8b949e;
        font-weight: 600;
        padding: 0 16px;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #21262D;
        color: #FFFFFF;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    /* Force Dark Background for Visibility */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }

    /* Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        border-color: rgba(78, 205, 196, 0.5);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .job-title {
        font-size: 1.3rem;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #FFF, #AAA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }
    
    .company-name {
        font-size: 0.95rem;
        color: #8B949E;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .tag-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 20px;
    }
    
    .glass-tag {
        background: rgba(78, 205, 196, 0.1);
        color: #4ECDC4;
        padding: 4px 12px;
        border-radius: 100px;
        font-size: 0.8rem;
        border: 1px solid rgba(78, 205, 196, 0.2);
    }
    
    .apply-btn-glow {
        display: block;
        width: 100%;
        text-align: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.2s;
    }
    .apply-btn-glow:hover {
        background: #4ECDC4;
        color: #000;
        border-color: #4ECDC4;
        box-shadow: 0 0 15px rgba(78, 205, 196, 0.4);
    }

    /* Resume Container - Dark Mode Notion Style */
    .resume-dark {
        background: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 40px;
        color: #E6E6E6;
        font-family: 'Inter', sans-serif;
        line-height: 1.7;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.2);
    }
    .resume-dark h3 {
        color: #4ECDC4;
        border-bottom: 1px solid #30363D;
        padding-bottom: 8px;
        margin-top: 24px;
    }
    
    /* Email Window - Futuristic */
    .email-future {
        background: #0D1117;
        border: 1px solid #30363D;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .email-top-bar {
        background: #161B22;
        padding: 12px 20px;
        border-bottom: 1px solid #30363D;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .email-content {
        padding: 24px;
        color: #C9D1D9;
        font-family: 'Space Grotesk', monospace;
        line-height: 1.6;
    }
    
</style>
""", unsafe_allow_html=True)

# --- Title & Styling ---
st.markdown("""
<div style="text-align: center; margin-bottom: 40px;">
    <h1 style="font-size: 3.5rem; font-weight: 800; background: linear-gradient(90deg, #FF6B6B, #4ECDC4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0;">JobHunter Pro</h1>
    <p style="color: #8B949E; font-size: 1.2rem; margin-top: 10px; letter-spacing: 1px;">AI-POWERED • CAREER • ORCHESTRATION</p>
</div>
""", unsafe_allow_html=True)

# --- Mission Control (Top Bar) ---
with st.container():
    st.markdown("<div style='background: #161B22; padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #E6E6E6; margin-top: 0;'>Mission Control</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        job_role = st.text_input("Target Role", value="Python Developer", placeholder="e.g. Data Scientist")
    with col2:
        location = st.text_input("Target Location", value="Remote", placeholder="e.g. San Francisco")
    with col3:
        experience = st.selectbox(
            "Experience Level", 
            options=["0-1 Years", "1-3 Years", "3-5 Years", "5+ Years"],
            index=1
        )
        
    resume_content = st.text_area(
        "Candidate DNA (Master Resume)", 
        height=150, 
        placeholder="Paste your resume content here. The agents will analyze this to match jobs and tailor applications...",
        help="Paste your full text resume here."
    )
    
    st.markdown("<div style='height: 10px'></div>", unsafe_allow_html=True)
    start_btn = st.button("⚡ Initialize Agents", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Main Area ---
tab1, tab2, tab3 = st.tabs(["🔴 Live Operations", "🔍 Insights Grid", "📦 Application Assets"])

if start_btn:
    if not resume_content:
        st.error("Please paste your resume content in the Candidate DNA section!")
    else:
        # Check if Ollama is accessible (simple check)
        try:
            pass 
        except Exception:
            pass

        with tab1:
            st.info(f"Initializing Agent Swarm for level: {experience}...")
            
            with st.spinner("Executing Mission: Scouting -> Strategizing -> Drafting"):
                try:
                    # Pass experience level to Crew
                    job_crew = JobHunterCrew(job_role, location, experience, resume_content)
                    final_result = job_crew.run()
                    st.success("Mission Accomplished.")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.markdown("Is access to Ollama enabled? Make sure running `ollama serve`.")
                    # Fallback/Debug info
                    st.write(e)
                    final_result = None

        if final_result:
            # --- Tab 2: Jobs ---
            with tab2:
                st.markdown("#### 🔍 Detected Opportunities")
                
                # Try to get the output of the first task (Search Task)
                jobs_data = []
                try:
                    # SIDE CHANNEL: Check for direct tool output file first
                    import os
                    if os.path.exists("jobs_output.json"):
                         with open("jobs_output.json", "r") as f:
                              try:
                                  jobs_data = json.load(f)
                              except:
                                  pass

                    # Fallback to Agent Output if file not found or empty
                    if not jobs_data and hasattr(final_result, 'tasks_output') and len(final_result.tasks_output) > 0:
                        search_output = final_result.tasks_output[0]
                        if hasattr(search_output, 'json_dict') and search_output.json_dict:
                            jobs_data = search_output.json_dict.get('jobs', [])
                        elif hasattr(search_output, 'pydantic') and search_output.pydantic:
                            jobs_data = search_output.pydantic.jobs
                        elif hasattr(search_output, 'raw'):
                             # Fallback: try to parse raw string if it looks like JSON
                            import json
                            import re
                            try:
                                raw_text = search_output.raw
                                # Strip markdown code blocks if present
                                match = re.search(r'```json\n?(.*?)\n?```', raw_text, re.DOTALL)
                                if match:
                                    raw_text = match.group(1)
                                
                                jobs_data = json.loads(raw_text)
                            except:
                                st.warning("Could not parse job data JSON.")
                                st.text(search_output.raw)

                    if jobs_data:
                        # Render HTML Cards
                        
                        # Handle Pydantic objects or dicts
                        jobs_list = []
                        
                        # Normalize dict to list if needed
                        if isinstance(jobs_data, dict):
                            if 'results' in jobs_data:
                                jobs_data = jobs_data['results']
                            elif 'jobs' in jobs_data:
                                jobs_data = jobs_data['jobs']
                            elif 'data' in jobs_data:
                                jobs_data = jobs_data['data']
                            else:
                                # Try to find any list value
                                for v in jobs_data.values():
                                    if isinstance(v, list):
                                        jobs_data = v
                                        break
                        
                        if len(jobs_data) > 0:
                             if hasattr(jobs_data[0], 'model_dump'):
                                 jobs_list = [j.model_dump() for j in jobs_data]
                             else:
                                 jobs_list = jobs_data
                        
                        # Grid Layout
                        cols = st.columns(3)
                        for i, job in enumerate(jobs_list):
                            with cols[i % 3]:
                                title = job.get('title', 'N/A')
                                company = job.get('company', 'N/A')
                                location = job.get('location', 'N/A')
                                salary = job.get('salary', 'N/A')
                                link = job.get('link', '#')
                                
                                # Using standard string formatting to avoid indentation issues
                                # Using standard string formatting to avoid indentation issues
                                card_html = textwrap.dedent(f'''
                                    <div class="glass-card">
                                        <div class="job-title">{title}</div>
                                        <div class="company-name">🏢 {company}</div>
                                        <div class="tag-container">
                                            <span class="glass-tag">📍 {location}</span>
                                            <span class="glass-tag">💰 {salary}</span>
                                        </div>
                                ''')
                                
                                # Check for valid link
                                if link and link.lower() not in ['n/a', '#', 'none', '']:
                                    card_html += textwrap.dedent(f'''
                                        <a href="{link}" target="_blank" class="apply-btn-glow">View Position</a>
                                    ''')
                                else:
                                    card_html += textwrap.dedent(f'''
                                        <div class="apply-btn-glow" style="opacity: 0.5; cursor: not-allowed; background: rgba(255,255,255,0.05);">Link Unavailable</div>
                                    ''')
                                
                                card_html += "</div>"
                                
                                # Remove newlines and extra spaces to ensure Clean Markdown rendering
                                st.markdown(card_html, unsafe_allow_html=True)
                                
                    else:
                        st.warning("No structured job data found in agent output.")
                except Exception as e:
                    import traceback
                    st.error(f"Error displaying jobs: {e}")
                    st.text(traceback.format_exc())
                    if 'jobs_data' in locals():
                        st.write("Jobs Data Type:", type(jobs_data))
                        st.write("Jobs Data Content:", str(jobs_data)[:500])
                    st.write(final_result)

            # --- Tab 3: Application Kit ---
            with tab3:
                cols = st.columns(2)
                
                # Extract Pydantic object if available
                email_content = None
                if hasattr(final_result, 'pydantic') and final_result.pydantic:
                    email_content = final_result.pydantic
                elif hasattr(final_result, 'json_dict') and final_result.json_dict:
                    email_content = final_result.json_dict
                
                with cols[0]:
                    st.markdown("""
                    <div class="resume-dark">
                        <div style="font-size: 1.2rem; font-weight: 700; color: #FFF; margin-bottom: 20px;">📄 Tailored Strategy</div>
                        <h3>Professional Profile</h3>
                        <p><i>The tailored summary based on the job requirements would appear here, optimized for ATS parsers...</i></p>
                        
                        <h3>Skill Matrix</h3>
                        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;">
                            <span style="background: #21262D; padding: 4px 12px; border-radius: 4px; border: 1px solid #30363D;">Python</span>
                            <span style="background: #21262D; padding: 4px 12px; border-radius: 4px; border: 1px solid #30363D;">AI Agents</span>
                            <span style="background: #21262D; padding: 4px 12px; border-radius: 4px; border: 1px solid #30363D;">Streamlit</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with cols[1]:
                    
                    email_body = "No content generated."
                    subject = "No subject"
                    
                    if email_content:
                        if hasattr(email_content, 'model_dump'):
                            data = email_content.model_dump()
                            email_body = data.get('email_body', '')
                            subject = data.get('subject_line', '')
                        else:
                            email_body = email_content.get('email_body', '')
                            subject = email_content.get('subject_line', '')
                    else:
                        email_body = str(final_result)
                    
                    st.markdown(f"""
                    <div class="email-future">
                         <div class="email-top-bar">
                             <div style="display: flex; gap: 6px;">
                                <div style="width: 10px; height: 10px; border-radius: 50%; background: #FF5F56;"></div>
                                <div style="width: 10px; height: 10px; border-radius: 50%; background: #FFBD2E;"></div>
                                <div style="width: 10px; height: 10px; border-radius: 50%; background: #27C93F;"></div>
                             </div>
                             <div style="color: #8B949E; font-size: 0.8rem;">DRAFT_V1.txt</div>
                         </div>
                         <div class="email-content">
                            <div style="color: #8B949E; margin-bottom: 4px;">To: <span style="color: #E6E6E6;">Hiring Manager</span></div>
                            <div style="color: #8B949E; margin-bottom: 20px;">Sub: <span style="color: #E6E6E6;">{subject}</span></div>
                            <div style="border-top: 1px solid #30363D; margin-bottom: 20px;"></div>
                            {email_body}
                         </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Download Button
                st.markdown("<div style='height: 40px'></div>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Export Application Assets",
                    data=str(final_result.raw) if hasattr(final_result, 'raw') else str(final_result),
                    file_name="job_application_assets.txt",
                    mime="text/plain",
                    type="primary"
                )

else:
    with tab1:
        st.info("System Ready. Initialize parameters in Mission Control.")
