import os
import requests
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from utils.logger import get_tracing_logger

# Load environment variables from .env file
load_dotenv()

# Constants for RapidAPI
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = "jsearch.p.rapidapi.com"
JSEARCH_URL = "https://jsearch.p.rapidapi.com/search"

def fetch_jobs(keyword: str, request_id: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
    """
    Fetches job listings from JSearch API via RapidAPI.
    
    Args:
        keyword (str): Search term for job listings.
        request_id (str, optional): Unique ID for request tracing.
        
    Returns:
        list: A list of cleaned job dictionaries or an empty list on failure.
    """
    # Start a tracing logger for this request
    logger = get_tracing_logger("job_fetcher", request_id=request_id)
    logger.info(f"Starting job fetch for keyword: {keyword}")

    if not RAPIDAPI_KEY:
        logger.error("RAPIDAPI_KEY not found in environment variables.")
        return []

    # API headers and parameters
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    params = {
        "query": keyword,
        "num_pages": "1",
        "page": "1"
    }

    try:
        # Perform the API request
        logger.info(f"Calling JSearch API at {JSEARCH_URL}")
        response = requests.get(JSEARCH_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        jobs_data = data.get("data", [])
        
        # Clean and map the results
        cleaned_jobs = []
        for job in jobs_data:
            cleaned_job = {
                "job_title": job.get("job_title"),
                "company_name": job.get("employer_name"),
                "location": f"{job.get('job_city', '')}, {job.get('job_state', '')}, {job.get('job_country', '')}".strip(", "),
                "is_remote": job.get("job_is_remote", False),
                "date_posted": job.get("job_posted_at_datetime_utc"),
                "apply_link": job.get("job_apply_link")
            }
            cleaned_jobs.append(cleaned_job)
            
        logger.info(f"Successfully fetched {len(cleaned_jobs)} jobs.")
        return cleaned_jobs

    except requests.exceptions.RequestException as e:
        # Centralized logging for failure
        logger.error(f"API call failed: {str(e)}")
        return None
    except Exception as e:
        # General error handling
        logger.error(f"An unexpected error occurred: {str(e)}")
        return None
