import json
import os


def load_contacts(filename):
    """Load contacts from a JSON file."""

    if not os.path.exists(filename):
        return []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("File contains invalid JSON.")
        return []

    except Exception as error:
        print(f"Error loading file: {error}")
        return []


def save_contacts(filename, contacts):
    """Save contacts to a JSON file."""

    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(
                contacts,
                file,
                ensure_ascii=False,
                indent=4
            )

        print("Contacts successfully saved.")

    except Exception as error:
        print(f"Error saving file: {error}")