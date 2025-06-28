from fastapi import FastAPI,BackgroundTasks
app = FastAPI()
from scraper_app.core.scraper import run_scraper
from scraper_app.db.db_connection import get_progress,create_connection,close_connection
from scraper_app.utils.constants import dates
@app.post("/scrape-data")
def get_train_data(date: list[str],background_tasks: BackgroundTasks):
    if date == ["string"] or date == []:
        date = dates
    # background_tasks.add_task(run_scraper, date)
    res = run_scraper(date)
    return res

@app.post("/get-progress")
def get_progress_from_db():
    client = create_connection()
    progress = get_progress(client)
    close_connection(client=client)
    return progress
@app.get("/")
def health_check():
    return {"msg":"Scraper apis running fine"}
    