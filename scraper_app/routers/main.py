from fastapi import FastAPI,BackgroundTasks
app = FastAPI()
from scraper_app.core.scraper import run_scraper
from scraper_app.db.db_connection import get_progress,create_connection,close_connection
from scraper_app.utils.constants import dates
from scraper_app.utils.util import generate_correlation_id
from scraper_app.core.test import main
from scraper_app.wrappers.scraper_wrapper import scraper_wrapper_helper

from scraper_app.schemas.scraper_schemas import Date

from scraper_app.wrappers.scraper_wrapper import scraper_wrapper_helper
@app.post("/scrape-data")
def get_train_data(date: Date,background_tasks: BackgroundTasks):
    correlation_id = generate_correlation_id()
    scraper_wrapper_helper(date,background_tasks,correlation_id)
    
    # main()
    # res = run_scraper(correlation_id,date)
    return {"correlation_id":correlation_id}

@app.get("/get-progress")
def get_progress_from_db(correlation_id):
    client = create_connection()
    progress = get_progress(client,correlation_id)
    close_connection(client=client)
    return progress
@app.get("/")
def health_check():
    return {"msg":"Scraper apis running fine"}
    