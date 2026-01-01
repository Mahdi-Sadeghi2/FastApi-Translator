from openai import OpenAI
from sqlalchemy.orm import Session
from crud import update_translation_task
from dotenv import load_dotenv
import os
import time

# Load environment variables from the .env file
load_dotenv()

# Initialize the OpenAI client using the API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def perform_translation(task_id: int, text: str, languages: list, db: Session):
    """
    Performs translation of the given text into multiple languages
    and updates the translation task in the database.

    This function is intended to run as a background task.
    """
    translations = {}

    # Loop through each requested target language
    for lang in languages:
        try:
            # Build a strict prompt to ensure only translated text is returned
            prompt = (
                f"Translate the following text to {lang}. "
                f"Only return the translation, no explanations.\n\n{text}"
            )

            # Call OpenAI Chat Completion API to generate the translation
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Lightweight, fast, and cost-effective model
                messages=[
                    # System message defines the model's role/behavior
                    {"role": "system", "content": "You are a professional translator."},
                    # User message contains the actual translation request
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,  # Low temperature for consistent, literal translations
            )

            # Extract the translated text from the API response
            translated_text = response.choices[0].message.content.strip()
            translations[lang] = translated_text

            # Log a short preview of the translation
            print(f"Translated to {lang}: {translated_text[:50]}...")

        except Exception as e:
            # Handle and store any errors that occur during translation
            print(f"Error translating to {lang}: {e}")
            translations[lang] = f"Error: {str(e)}"

        # Small delay to reduce the risk of hitting API rate limits
        time.sleep(1)

    # Update the translation task in the database with all results
    update_translation_task(db, task_id, translations)

    # Final log indicating task completion
    print(
        f"Task {task_id} completed with translations for {len(languages)} languages"
    )
