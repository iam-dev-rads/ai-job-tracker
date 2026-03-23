def format_remote_status(is_remote: bool) -> str:
    """
    Converts a boolean remote status to a human-readable string.
    """
    return "Remote" if is_remote else "Onsite"

def format_date(date_str: str) -> str:
    """
    Formats the date string (e.g., ISO format) for display.
    """
    if not date_str or not isinstance(date_str, str):
        return "N/A"
    
    # Return YYYY-MM-DD from the timestamp (e.g., "2024-03-22T12:00:00")
    return date_str.split("T")[0]
