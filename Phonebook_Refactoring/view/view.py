from model.contact import Contact


class View:
    """Handles all interaction with the user."""

    @staticmethod
    def show_menu() -> str:
        """
        Display the main menu.

        Returns:
            Selected menu item.
        """

        print("\n" + "=" * 40)
        print("PHONEBOOK")
        print("=" * 40)
        print("1. Open file")
        print("2. Save file")
        print("3. Show all contacts")
        print("4. Create contact")
        print("5. Find contact")
        print("6. Edit contact")
        print("7. Delete contact")
        print("8. Exit")

        return input("\nChoose menu item: ").strip()

    @staticmethod
    def show_message(message: str) -> None:
        """
        Display an information message.

        Args:
            message: Message text.
        """

        print(message)

    @staticmethod
    def show_error(message: str) -> None:
        """
        Display an error message.

        Args:
            message: Error text.
        """

        print(f"Error: {message}")

    @staticmethod
    def show_contacts(contacts: list[Contact]) -> None:
        """
        Display a list of contacts.

        Args:
            contacts: Contacts to display.
        """

        if not contacts:
            print("Contact list is empty.")
            return

        print()

        for contact in contacts:
            print(contact)
            print("-" * 40)

    @staticmethod
    def input_contact() -> tuple[str, str, str]:
        """
        Request contact information.

        Returns:
            Tuple containing name, phone and comment.
        """

        print("\nEnter contact information:")

        name = input("Name: ").strip()
        phone = input("Phone: ").strip()
        comment = input("Comment: ").strip()

        return name, phone, comment

    @staticmethod
    def input_contact_id() -> int:
        """
        Request a contact ID.

        Returns:
            Contact ID.
        """

        value = input("Enter contact ID: ").strip()

        while not value.isdigit():
            print("Please enter a valid number.")
            value = input("Enter contact ID: ").strip()

        return int(value)

    @staticmethod
    def input_search_text() -> str:
        """
        Request search text.

        Returns:
            Search string.
        """

        return input("Search: ").strip()

    @staticmethod
    def confirm(message: str) -> bool:
        """
        Request confirmation.

        Args:
            message: Confirmation message.

        Returns:
            True if confirmed, otherwise False.
        """

        answer = input(f"{message} (y/n): ").strip().lower()

        return answer == "y"