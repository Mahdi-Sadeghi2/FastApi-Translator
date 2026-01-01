from fastapi import FastAPI, BackgroundTasks, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
import schemas
import crud
import models
from database import get_db, engine
from sqlalchemy.orm import Session
from utils import perform_translation

# Create database tables if they do not exist
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI()

# Configure Jinja2 templates for HTML rendering
templates = Jinja2Templates(directory="templates")

# Enable CORS (allows requests from any origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def read_root():
    """
    Basic health-check endpoint.
    """
    return {"message": "Translation Service API"}


@app.get('/index', response_class=HTMLResponse)
def index(request: Request):
    """
    Serves the main HTML page.
    """
    return templates.TemplateResponse(
        'index.html',
        {'request': request}
    )


@app.post('/translate', response_model=schemas.TaskResponse)
def translate(
    request: schemas.TranslationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Creates a translation task and schedules translation
    to run asynchronously in the background.
    """
    task = crud.create_translation_task(
        db,
        request.text,
        request.languages
    )

    # Run translation asynchronously so the request returns immediately
    background_tasks.add_task(
        perform_translation,
        task.id,
        request.text,
        request.languages,
        db
    )

    # Initial response does not include translations yet
    return {
        "task_id": task.id,
        "status": task.status,
        "translations": {}
    }


@app.get('/translate/{task_id}')
def get_translate(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the full translation task by ID.
    """
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.get('/translate/content/{task_id}')
def get_translate_content(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieves translation task content (same as /translate/{task_id}).
    """
    task = crud.get_translation_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task
