# Translation Service App

A simple web-based translation service built with **FastAPI**,
**SQLAlchemy**, and **OpenAI**, featuring a lightweight **HTML +
Bootstrap** frontend.

The app allows users to submit text for translation into multiple
languages, processes translations asynchronously in the background, and
stores results in a database.

------------------------------------------------------------------------

## Features

-   Translate text into multiple languages
-   Background processing (non-blocking requests)
-   Persistent storage using a database
-   Simple web UI (HTML + Bootstrap)
-   Check translation status and content by task ID
-   REST API endpoints for integration

------------------------------------------------------------------------

## Tech Stack

### Backend

-   Python
-   FastAPI
-   SQLAlchemy
-   OpenAI API
-   SQLite / PostgreSQL (via SQLAlchemy)
-   Pydantic

### Frontend

-   HTML
-   Bootstrap 5
-   Axios

------------------------------------------------------------------------

## Project Structure

    .
    ├── main.py
    ├── utils.py
    ├── crud.py
    ├── models.py
    ├── schemas.py
    ├── database.py
    ├── templates/
    │   └── index.html
    ├── .env
    └── README.md

------------------------------------------------------------------------

## Environment Variables

Create a `.env` file in the project root:

    OPENAI_API_KEY=your_openai_api_key_here
    DATABASE_URL=sqlite:///./translations.db

------------------------------------------------------------------------

## How to Run the App

1.  Install dependencies:

```{=html}
<!-- -->
```
    pip install fastapi uvicorn sqlalchemy python-dotenv openai

2.  Start the server:

```{=html}
<!-- -->
```
    uvicorn main:app --reload

3.  Open in browser:

```{=html}
<!-- -->
```
    http://127.0.0.1:8000/index

------------------------------------------------------------------------

## How to Use the App (Simple Explanation)

1.  Open the web page.
2.  Enter text to translate.
3.  Enter target languages (comma-separated, e.g. `es, fr, de`).
4.  Click **Translate**.
5.  Copy the generated Task ID.
6.  Use the Task ID to check status or view translated content.

------------------------------------------------------------------------

## API Endpoints

-   POST `/translate`
-   GET `/translate/{task_id}`
-   GET `/translate/content/{task_id}`

------------------------------------------------------------------------

## Notes

-   Translations run in the background.
-   Results are stored in the database.
-   Requires a valid OpenAI API key.

------------------------------------------------------------------------

## License

Educational / demo use.
