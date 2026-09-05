import json
import os

from model.contact import Contact
from model.exceptions import (
    FileReadError,
    FileWriteError
)


class FileManager:
    """Handles loading and saving contacts to JSON files."""

    def load_contacts(self, filename: str) -> list[Contact]:
        """
        Load contacts from a JSON file.

        Args:
            filename: Path to JSON file.

        Returns:
            List of Contact objects.

        Raises:
            FileReadError: If the file cannot be read.
        """

        if not os.path.exists(filename):
            return []

        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            return [
                Contact.from_dict(item)
                for item in data
            ]

        except json.JSONDecodeError as error:
            raise FileReadError(
                "The file contains invalid JSON."
            ) from error

        except OSError as error:
            raise FileReadError(
                f"Unable to read file '{filename}'."
            ) from error

    def save_contacts(
        self,
        filename: str,
        contacts: list[Contact]
    ) -> None:
        """
        Save contacts to a JSON file.

        Args:
            filename: Path to JSON file.
            contacts: List of Contact objects.

        Raises:
            FileWriteError: If the file cannot be written.
        """

        try:
            data = [
                contact.to_dict()
                for contact in contacts
            ]

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except OSError as error:
            raise FileWriteError(
                f"Unable to save file '{filename}'."
            ) from error