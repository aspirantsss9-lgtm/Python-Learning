from typing import Self


class Contact:
    """Represents a single contact in the phonebook."""

    def __init__(
        self,
        contact_id: int,
        name: str,
        phone: str,
        comment: str
    ) -> None:
        """
        Initialize a contact.

        Args:
            contact_id: Unique contact identifier.
            name: Contact name.
            phone: Contact phone number.
            comment: Additional comment.
        """

        self.id = contact_id
        self.name = name
        self.phone = phone
        self.comment = comment

    def to_dict(self) -> dict:
        """
        Convert the contact to a dictionary.

        Returns:
            Dictionary representation of the contact.
        """

        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "comment": self.comment
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """
        Create a Contact object from a dictionary.

        Args:
            data: Dictionary containing contact data.

        Returns:
            Contact object.
        """

        return cls(
            contact_id=data["id"],
            name=data["name"],
            phone=data["phone"],
            comment=data["comment"]
        )

    def __str__(self) -> str:
        """
        Return a readable string representation.

        Returns:
            Formatted contact string.
        """

        return (
            f"ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Phone: {self.phone}\n"
            f"Comment: {self.comment}"
        )