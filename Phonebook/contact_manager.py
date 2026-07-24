def generate_id(contacts):
    """Generate unique contact ID."""

    if not contacts:
        return 1

    return max(contact["id"] for contact in contacts) + 1


def show_contacts(contacts):
    """Display all contacts."""

    if not contacts:
        print("Contact list is empty.")
        return

    for contact in contacts:
        print("-" * 40)
        print(f"ID: {contact['id']}")
        print(f"Name: {contact['name']}")
        print(f"Phone: {contact['phone']}")
        print(f"Comment: {contact['comment']}")

    print("-" * 40)


def create_contact(contacts):
    """Create new contact."""

    name = input("Enter name: ").strip()

    while not name:
        print("Name cannot be empty.")
        name = input("Enter name: ").strip()

    phone = input("Enter phone: ").strip()

    while not phone.replace("+", "").isdigit():
        print("Phone must contain only digits.")
        phone = input("Enter phone: ").strip()

    comment = input("Enter comment: ").strip()

    contact = {
        "id": generate_id(contacts),
        "name": name,
        "phone": phone,
        "comment": comment
    }

    contacts.append(contact)

    print("Contact added.")


def find_contacts(contacts):
    """Search contacts."""

    search_text = input(
        "Enter search text: "
    ).strip().lower()

    results = []

    for contact in contacts:

        searchable_text = (
            f"{contact['id']} "
            f"{contact['name']} "
            f"{contact['phone']} "
            f"{contact['comment']}"
        ).lower()

        if search_text in searchable_text:
            results.append(contact)

    if not results:
        print("No contacts found.")
        return

    show_contacts(results)


def get_contact_by_id(contacts, contact_id):
    """Return contact by ID."""

    for contact in contacts:
        if contact["id"] == contact_id:
            return contact

    return None


def edit_contact(contacts):
    """Edit existing contact."""

    if not contacts:
        print("Contact list is empty.")
        return

    try:
        contact_id = int(
            input("Enter contact ID: ")
        )

    except ValueError:
        print("Invalid ID.")
        return

    contact = get_contact_by_id(
        contacts,
        contact_id
    )

    if contact is None:
        print("Contact not found.")
        return

    print("Leave field empty to keep value.")

    new_name = input(
        f"Name [{contact['name']}]: "
    ).strip()

    new_phone = input(
        f"Phone [{contact['phone']}]: "
    ).strip()

    new_comment = input(
        f"Comment [{contact['comment']}]: "
    ).strip()

    if new_name:
        contact["name"] = new_name

    if new_phone:

        if not new_phone.replace("+", "").isdigit():
            print("Invalid phone format.")
            return

        contact["phone"] = new_phone

    if new_comment:
        contact["comment"] = new_comment

    print("Contact updated.")


def delete_contact(contacts):
    """Delete contact."""

    if not contacts:
        print("Contact list is empty.")
        return

    try:
        contact_id = int(
            input("Enter contact ID: ")
        )

    except ValueError:
        print("Invalid ID.")
        return

    contact = get_contact_by_id(
        contacts,
        contact_id
    )

    if contact is None:
        print("Contact not found.")
        return

    confirmation = input(
        f"Delete '{contact['name']}'? (y/n): "
    ).lower()

    if confirmation == "y":
        contacts.remove(contact)
        print("Contact deleted.")
    else:
        print("Deletion cancelled.")