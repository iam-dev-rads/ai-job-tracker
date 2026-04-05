def format_remote_status(is_remote: bool) -> str:
    """
    Converts a boolean remote status to a human-readable string.
    """
    return "Remote" if is_remote else "Onsite"

def format_date(date_str: str) -> str:
    """
    Formats the date string for display.
    Expects ISO 8601 format (e.g., "2024-03-22T12:00:00").
    """
    if not date_str or not isinstance(date_str, str):
        # Fallback if the date field is missing or malformed
        return "N/A"
    
    # Extract the date part (YYYY-MM-DD) before the time separator 'T'
    return date_str.split("T")[0]
