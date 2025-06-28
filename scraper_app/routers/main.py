from fastapi import FastAPI,BackgroundTasks
app = FastAPI()
from scraper_app.core.scraper import run_scraper
from scraper_app.db.db_connection import get_progress,create_connection,close_connection
from scraper_app.utils.constants import dates
from scraper_app.utils.util import generate_correlation_id
@app.post("/scrape-data")
def get_train_data(date: list[str],background_tasks: BackgroundTasks):
    correlation_id = generate_correlation_id()
    if date == ["string"] or date == []:
        date = dates
    background_tasks.add_task(run_scraper,correlation_id, date)
    # res = run_scraper(correlation_id,date)
    return {"correlation_id":correlation_id}

@app.post("/get-progress")
def get_progress_from_db(correlation_id):
    client = create_connection()
    progress = get_progress(client,correlation_id)
    close_connection(client=client)
    return progress
@app.get("/")
def health_check():
    return {"msg":"Scraper apis running fine"}
    