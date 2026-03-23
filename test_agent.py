from agents.job_fetcher import fetch_jobs

def test_fetch():
    print("Testing fetch_jobs('Python developer')...")
    # This will likely fail if RAPIDAPI_KEY is not set in .env,
    # but we can check the logs for proper error handling.
    jobs = fetch_jobs("Python developer")
    if jobs:
        print(f"Found {len(jobs)} jobs.")
        for i, job in enumerate(jobs[:3]):
            print(f"Job {i+1}: {job['job_title']} at {job['company_name']}")
    else:
        print("No jobs found or error occurred. Check the console logs.")

if __name__ == "__main__":
    test_fetch()
