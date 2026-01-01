from sqlalchemy.orm import Session
import models


def create_translation_task(db: Session, text: str, languages: list):
    """
    Creates a new translation task record in the database.

    - `text`: source text to be translated
    - `languages`: list of target languages
    - Initial task status is handled by the model defaults
    """
    task = models.TranslationTask(text=text, languages=languages)
    db.add(task)          # Add task to the current database session
    db.commit()           # Persist the task to the database
    db.refresh(task)      # Reload task to populate generated fields (e.g., ID)
    return task


def get_translation_task(db: Session, task_id: int):
    """
    Retrieves a translation task by its unique ID.

    Returns:
    - TranslationTask object if found
    - None if no matching task exists
    """
    return db.query(models.TranslationTask).filter(
        models.TranslationTask.id == task_id
    ).first()


def update_translation_task(db: Session, task_id: int, translations: dict):
    """
    Updates an existing translation task with its completed translations.

    - `translations`: dictionary mapping language → translated text
    - Sets task status to 'completed'
    """
    task = db.query(models.TranslationTask).filter(
        models.TranslationTask.id == task_id
    ).first()

    task.translations = translations  # Save translation results
    task.status = "completed"         # Mark task as finished

    db.commit()       # Persist changes
    db.refresh(task)  # Reload updated task from database
    return task
