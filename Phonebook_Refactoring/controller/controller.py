from model.file_manager import FileManager
from model.phonebook import PhoneBook
from model.exceptions import PhoneBookError
from view.view import View


class Controller:
    """Coordinates interaction between the model and the view."""

    def __init__(self) -> None:
        """Initialize controller."""

        self.phonebook = PhoneBook()
        self.file_manager = FileManager()
        self.view = View()

        self.filename = "contacts.json"
        self.is_running = True

    def run(self) -> None:
        """Run the main application loop."""

        while self.is_running:

            choice = self.view.show_menu()

            try:

                match choice:

                    case "1":
                        self.open_file()

                    case "2":
                        self.save_file()

                    case "3":
                        self.show_contacts()

                    case "4":
                        self.create_contact()

                    case "5":
                        self.find_contacts()

                    case "6":
                        self.edit_contact()

                    case "7":
                        self.delete_contact()

                    case "8":
                        self.exit_program()

                    case _:
                        self.view.show_error("Invalid menu item.")

            except PhoneBookError as error:
                self.view.show_error(str(error))

            except Exception as error:
                self.view.show_error(f"Unexpected error: {error}")

    def open_file(self) -> None:
        """Load contacts from file."""

        contacts = self.file_manager.load_contacts(self.filename)

        self.phonebook.load_contacts(contacts)

        self.view.show_message("Contacts loaded successfully.")

    def save_file(self) -> None:
        """Save contacts to file."""

        self.file_manager.save_contacts(
            self.filename,
            self.phonebook.get_all_contacts()
        )

        self.view.show_message("Contacts saved successfully.")

    def show_contacts(self) -> None:
        """Display all contacts."""

        contacts = self.phonebook.get_all_contacts()

        self.view.show_contacts(contacts)

    def create_contact(self) -> None:
        """Create a new contact."""

        name, phone, comment = self.view.input_contact()

        contact = self.phonebook.add_contact(
            name,
            phone,
            comment
        )

        self.view.show_message(
            f"Contact '{contact.name}' created."
        )

    def find_contacts(self) -> None:
        """Search contacts."""

        text = self.view.input_search_text()

        contacts = self.phonebook.find_contacts(text)

        self.view.show_contacts(contacts)

    def edit_contact(self) -> None:
        """Edit an existing contact."""

        contact_id = self.view.input_contact_id()

        name, phone, comment = self.view.input_contact()

        contact = self.phonebook.edit_contact(
            contact_id,
            name,
            phone,
            comment
        )

        self.view.show_message(
            f"Contact '{contact.name}' updated."
        )

    def delete_contact(self) -> None:
        """Delete a contact."""

        contact_id = self.view.input_contact_id()

        contact = self.phonebook.delete_contact(contact_id)

        self.view.show_message(
            f"Contact '{contact.name}' deleted."
        )

    def exit_program(self) -> None:
        """Exit the application."""

        self.is_running = False

        self.view.show_message("Goodbye!")