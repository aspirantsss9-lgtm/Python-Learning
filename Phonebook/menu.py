def show_menu():
    """Display main menu."""

    print("\n" + "=" * 40)
    print("PHONEBOOK")
    print("=" * 40)

    print("1. Open file")
    print("2. Save file")
    print("3. Show contacts")
    print("4. Create contact")
    print("5. Find contact")
    print("6. Edit contact")
    print("7. Delete contact")
    print("8. Exit")

    print("=" * 40)


def get_menu_choice():
    """Get menu choice."""

    while True:

        choice = input(
            "Choose menu item: "
        ).strip()

        if choice.isdigit():

            choice = int(choice)

            if 1 <= choice <= 8:
                return choice

        print("Invalid menu item.")