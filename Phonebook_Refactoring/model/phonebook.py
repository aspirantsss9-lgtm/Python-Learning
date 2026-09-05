from model.contact import Contact
from model.exceptions import (
    ContactNotFoundError,
    InvalidContactError,
    InvalidPhoneError
)


class PhoneBook:
    """Represents a phonebook containing contacts."""

    def __init__(self) -> None:
        """Initialize an empty phonebook."""

        self.contacts: list[Contact] = []

    def load_contacts(self, contacts: list[Contact]) -> None:
        """
        Replace the current contact list.

        Args:
            contacts: List of Contact objects.
        """

        self.contacts = contacts

    def get_all_contacts(self) -> list[Contact]:
        """
        Return all contacts.

        Returns:
            List of contacts.
        """

        return self.contacts

    def generate_id(self) -> int:
        """
        Generate a unique contact ID.

        Returns:
            New contact ID.
        """

        if not self.contacts:
            return 1

        return max(contact.id for contact in self.contacts) + 1

    def _validate_phone(self, phone: str) -> str:
        """
        Validate and normalize a phone number.

        Args:
            phone: Phone number to validate.

        Returns:
            Stripped phone number.

        Raises:
            InvalidPhoneError: If phone number is invalid.
        """

        phone = phone.strip()

        if not phone:
            raise InvalidPhoneError(
                "Phone number cannot be empty."
            )

        if phone.startswith("+"):
            phone_digits = phone[1:]
        else:
            phone_digits = phone

        if not phone_digits.isdigit():
            raise InvalidPhoneError(
                "Phone must contain only digits and an optional leading '+'."
            )

        return phone

    def add_contact(
        self,
        name: str,
        phone: str,
        comment: str
    ) -> Contact:
        """
        Add a new contact.

        Args:
            name: Contact name.
            phone: Contact phone number.
            comment: Contact comment.

        Returns:
            Created Contact object.

        Raises:
            InvalidContactError: If contact name is empty.
            InvalidPhoneError: If phone number is invalid.
        """

        name = name.strip()

        if not name:
            raise InvalidContactError(
                "Contact name cannot be empty."
            )

        phone = self._validate_phone(phone)

        contact = Contact(
            contact_id=self.generate_id(),
            name=name,
            phone=phone,
            comment=comment.strip()
        )

        self.contacts.append(contact)

        return contact

    def get_contact(self, contact_id: int) -> Contact | None:
        """
        Find a contact by ID.

        Args:
            contact_id: Contact ID.

        Returns:
            Contact object or None.
        """

        for contact in self.contacts:
            if contact.id == contact_id:
                return contact

        return None

    def edit_contact(
        self,
        contact_id: int,
        name: str,
        phone: str,
        comment: str
    ) -> Contact:
        """
        Edit an existing contact.

        Args:
            contact_id: Contact ID.
            name: New contact name.
            phone: New phone number.
            comment: New comment.

        Returns:
            Updated Contact object.

        Raises:
            ContactNotFoundError: If contact is not found.
            InvalidContactError: If contact name is empty.
            InvalidPhoneError: If phone number is invalid.
        """

        contact = self.get_contact(contact_id)

        if contact is None:
            raise ContactNotFoundError(
                "Contact not found."
            )

        name = name.strip()

        if not name:
            raise InvalidContactError(
                "Contact name cannot be empty."
            )

        phone = self._validate_phone(phone)

        contact.name = name
        contact.phone = phone
        contact.comment = comment.strip()

        return contact

    def delete_contact(self, contact_id: int) -> Contact:
        """
        Delete a contact.

        Args:
            contact_id: Contact ID.

        Returns:
            Deleted Contact object.

        Raises:
            ContactNotFoundError: If contact is not found.
        """

        contact = self.get_contact(contact_id)

        if contact is None:
            raise ContactNotFoundError(
                "Contact not found."
            )

        self.contacts.remove(contact)

        return contact

    def find_contacts(
        self,
        search_text: str
    ) -> list[Contact]:
        """
        Search contacts by all fields.

        Args:
            search_text: Text to search.

        Returns:
            List of matching contacts.
        """

        search_text = search_text.lower().strip()

        result: list[Contact] = []

        for contact in self.contacts:

            searchable = (
                f"{contact.id} "
                f"{contact.name} "
                f"{contact.phone} "
                f"{contact.comment}"
            ).lower()

            if search_text in searchable:
                result.append(contact)

        return result