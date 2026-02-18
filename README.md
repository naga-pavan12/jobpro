# JobHunter-Pro

A comprehensive Local AI Job Application System.

## Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com/) installed and running (`ollama serve`).
- The `llama3.1` model pulled (`ollama pull llama3.1`) or any other model specified in `src/agents.py`.

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```
2. Enter your Job Role, Location, and paste your Resume in the sidebar.
3. Click "Start Headhunting Crew".
