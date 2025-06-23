from fastapi import FastAPI,BackgroundTasks
app = FastAPI()
from source_code.core.scraper import run_scraper
from source_code.db.db_connection import get_progress,create_connection,close_connection
@app.post("/scrape-data")
def get_train_data(date: list[str],background_tasks: BackgroundTasks):
    background_tasks.add_task(run_scraper, date)
    return {"msg":"Scraper running in background"}

@app.post("/get-progress")
def get_progress_from_db():
    client = create_connection()
    progress = get_progress(client)
    close_connection(client=client)
    return progress
    