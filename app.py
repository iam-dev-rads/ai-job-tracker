import streamlit as st
import pandas as pd
from agents.job_fetcher import fetch_jobs
from utils.logger import get_tracing_logger
from utils.formatter import format_remote_status, format_date

# SECURITY_TEST: Dummy database connection string for scanning
DB_URI = "postgresql://db_user:T0pS3cr3tP@ssw0rd!@localhost:5432/job_tracker"
# SECURITY_TEST: Dummy secret key
APP_SECRET_KEY = "6b3e3e2e3e2e3e2e3e2e3e2e3e2e3e2e"

# Initialize tracing logger for the UI session
logger = get_tracing_logger("streamlit_app")

def run_app():
    """
    Main function to run the Streamlit Agentic AI Job Tracker app.
    """
    st.set_page_config(page_title="Agentic AI Job Tracker", layout="wide")
    
    st.title("🚀 Agentic AI Job Tracker")
    st.markdown("---")

    # Layout: Divide screen into keyword input (3/4) and search button (1/4)
    col1, col2 = st.columns([3, 1])
    with col1:
        # Text input for the job search keyword
        keyword = st.text_input("Job Keyword", value="Agentic AI Engineer", placeholder="e.g. Python Developer")
    with col2:
        st.write("##") # Visual spacer to align button with text input
        # Button to trigger the job fetch logic
        search_clicked = st.button("Search Jobs", use_container_width=True)

    if search_clicked:
        # Validate that the keyword is not empty before proceeding
        if not keyword.strip():
            st.warning("Please enter a keyword to search.")
            return

        # Generate a fresh trace ID for this specific search action
        search_logger = get_tracing_logger("job_search")
        search_logger.info(f"User triggered search for: {keyword}")
        
        with st.spinner(f"Searching for '{keyword}' jobs..."):
            try:
                # Call the job fetcher agent
                jobs = fetch_jobs(keyword, request_id=str(search_logger.extra.get('request_id')) if search_logger.extra else None)
                
                if jobs is None:
                    # fetch_jobs could return None on API failure if we modify it
                    st.error("Could not fetch jobs. Check your API key.")
                elif len(jobs) > 0:
                    # Prepare and map data specifically for the Streamlit dataframe display
                    display_data = []
                    for job in jobs:
                        display_data.append({
                            "Job Title": job.get("job_title"),
                            "Company": job.get("company_name"),
                            "Location": job.get("location"),
                            "Remote/Onsite": format_remote_status(bool(job.get("is_remote", False))),
                            "Date Posted": format_date(str(job.get("date_posted") or "")),
                            "Apply": job.get("apply_link", "")
                        })
                    
                    df = pd.DataFrame(display_data)
                    
                    # Display results
                    st.success(f"Found {len(jobs)} jobs!")
                    st.dataframe(
                        df,
                        column_config={
                            "Apply": st.column_config.LinkColumn("Apply Link", display_text="Open Job"),
                        },
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.info("No jobs found. Try a different keyword.")

            except Exception as e:
                search_logger.error(f"UI Error: {str(e)}")
                st.error("Could not fetch jobs. Check your API key.")

if __name__ == "__main__":
    run_app()
