
from scraper_app.core.scraper2 import run_scraper
def scraper_wrapper_helper(date,background_tasks,correlation_id):
    """used as a wrapper function for scraper"""
    try:
        if date == "string" or date == "":
            date = "08-08-2025"
        background_tasks.add_task(run_scraper,correlation_id, "08-08-2025")
    except Exception as e:
        raise e