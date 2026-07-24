from file_manager import (
    load_contacts,
    save_contacts
)

from contact_manager import (
    show_contacts,
    create_contact,
    find_contacts,
    edit_contact,
    delete_contact
)

from menu import (
    show_menu,
    get_menu_choice
)


DEFAULT_FILE = "contacts.json"


def main():

    contacts = []
    current_file = DEFAULT_FILE

    is_modified = False

    while True:

        show_menu()

        choice = get_menu_choice()

        if choice == 1:

            contacts = load_contacts(
                current_file
            )

            print(
                f"Loaded {len(contacts)} contacts."
            )

            is_modified = False

        elif choice == 2:

            save_contacts(
                current_file,
                contacts
            )

            is_modified = False

        elif choice == 3:

            show_contacts(contacts)

        elif choice == 4:

            create_contact(contacts)
            is_modified = True

        elif choice == 5:

            find_contacts(contacts)

        elif choice == 6:

            edit_contact(contacts)
            is_modified = True

        elif choice == 7:

            delete_contact(contacts)
            is_modified = True

        elif choice == 8:

            if is_modified:

                answer = input(
                    "Unsaved changes found. "
                    "Save before exit? (y/n): "
                ).lower()

                if answer == "y":

                    save_contacts(
                        current_file,
                        contacts
                    )

            print("Goodbye.")
            break


if __name__ == "__main__":
    main()
