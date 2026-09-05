import pytest

from model.contact import Contact
from model.exceptions import (
    ContactNotFoundError,
    FileReadError,
    FileWriteError,
    InvalidContactError,
    InvalidPhoneError,
)
from model.file_manager import FileManager
from model.phonebook import PhoneBook


def test_add_contact() -> None:
    phonebook = PhoneBook()

    contact = phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    assert contact.id == 1
    assert contact.name == "John Smith"
    assert contact.phone == "79991234567"
    assert contact.comment == "Friend"


def test_search_by_name() -> None:
    phonebook = PhoneBook()

    phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    result = phonebook.find_contacts("John")

    assert len(result) == 1
    assert result[0].name == "John Smith"


def test_search_by_phone() -> None:
    phonebook = PhoneBook()

    phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    result = phonebook.find_contacts("79991234567")

    assert len(result) == 1
    assert result[0].phone == "79991234567"


def test_general_search() -> None:
    phonebook = PhoneBook()

    phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Work"
    )

    result = phonebook.find_contacts("Work")

    assert len(result) == 1
    assert result[0].comment == "Work"


def test_edit_contact() -> None:
    phonebook = PhoneBook()

    contact = phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    updated_contact = phonebook.edit_contact(
        contact.id,
        "Mike Brown",
        "79161234567",
        "Colleague"
    )

    assert updated_contact.name == "Mike Brown"
    assert updated_contact.phone == "79161234567"
    assert updated_contact.comment == "Colleague"


def test_delete_contact() -> None:
    phonebook = PhoneBook()

    contact = phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    deleted_contact = phonebook.delete_contact(contact.id)

    assert deleted_contact.id == contact.id
    assert phonebook.get_all_contacts() == []


def test_get_contact() -> None:
    phonebook = PhoneBook()

    contact = phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    result = phonebook.get_contact(contact.id)

    assert result is not None
    assert result.name == "John Smith"


def test_invalid_phone() -> None:
    phonebook = PhoneBook()

    with pytest.raises(InvalidPhoneError):
        phonebook.add_contact(
            "John Smith",
            "invalid",
            "Friend"
        )


def test_edit_nonexistent_contact() -> None:
    phonebook = PhoneBook()

    with pytest.raises(ContactNotFoundError):
        phonebook.edit_contact(
            999,
            "John Smith",
            "79991234567",
            "Friend"
        )


def test_delete_nonexistent_contact() -> None:
    phonebook = PhoneBook()

    with pytest.raises(ContactNotFoundError):
        phonebook.delete_contact(999)


def test_search_nonexistent_contact() -> None:
    phonebook = PhoneBook()

    phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    result = phonebook.find_contacts("Alexander")

    assert result == []


def test_invalid_phone_when_adding_contact() -> None:
    phonebook = PhoneBook()

    with pytest.raises(InvalidPhoneError):
        phonebook.add_contact(
            "John Smith",
            "abc123",
            "Friend"
        )


def test_invalid_phone_when_editing_contact() -> None:
    phonebook = PhoneBook()

    contact = phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    with pytest.raises(InvalidPhoneError):
        phonebook.edit_contact(
            contact.id,
            "John Smith",
            "abc123",
            "Friend"
        )


def test_empty_phone_when_adding_contact() -> None:
    phonebook = PhoneBook()

    with pytest.raises(InvalidPhoneError):
        phonebook.add_contact(
            "John Smith",
            "",
            "Friend"
        )


def test_empty_contact() -> None:
    phonebook = PhoneBook()

    with pytest.raises(InvalidContactError):
        phonebook.add_contact(
            "",
            "",
            ""
        )


def test_invalid_contact_id_when_editing() -> None:
    phonebook = PhoneBook()

    with pytest.raises(ContactNotFoundError):
        phonebook.edit_contact(
            0,
            "John Smith",
            "79991234567",
            "Friend"
        )


def test_invalid_contact_id_when_deleting() -> None:
    phonebook = PhoneBook()

    with pytest.raises(ContactNotFoundError):
        phonebook.delete_contact(0)


def test_empty_name() -> None:
    phonebook = PhoneBook()

    with pytest.raises(InvalidContactError):
        phonebook.add_contact(
            "   ",
            "79991234567",
            "Friend"
        )


def test_search_with_empty_phonebook() -> None:
    phonebook = PhoneBook()

    result = phonebook.find_contacts("John")

    assert result == []


def test_search_with_empty_query() -> None:
    phonebook = PhoneBook()

    phonebook.add_contact(
        "John Smith",
        "79991234567",
        "Friend"
    )

    result = phonebook.find_contacts("")

    assert len(result) == 1


def test_delete_from_empty_phonebook() -> None:
    phonebook = PhoneBook()

    with pytest.raises(ContactNotFoundError):
        phonebook.delete_contact(1)


@pytest.mark.parametrize(
    "name",
    [
        "John",
        "John Smith",
        "Alexander Brown",
        "Иван Иванов",
        "Алексей",
    ],
)
def test_add_contact_with_different_names(name: str) -> None:
    phonebook = PhoneBook()

    contact = phonebook.add_contact(
        name,
        "79991234567",
        "Test"
    )

    assert contact.name == name


@pytest.mark.parametrize(
    "phone",
    [
        "79991234567",
        "+79991234567",
        "79161234567",
        "+79161234567",
        "1234567890",
    ],
)
def test_add_contact_with_different_phone_formats(phone: str) -> None:
    phonebook = PhoneBook()

    contact = phonebook.add_contact(
        "John Smith",
        phone,
        "Test"
    )

    assert contact.phone == phone


@pytest.mark.parametrize(
    "phone",
    [
        "abc",
        "abc123",
        "12+34",
        "++79991234567",
        "+",
        "79-99-123-45-67",
    ],
)
def test_add_contact_with_invalid_phone_formats(phone: str) -> None:
    phonebook = PhoneBook()

    with pytest.raises(InvalidPhoneError):
        phonebook.add_contact(
            "John Smith",
            phone,
            "Test"
        )


def test_contact_to_dict() -> None:
    contact = Contact(
        1,
        "John Smith",
        "79991234567",
        "Friend"
    )

    result = contact.to_dict()

    assert result == {
        "id": 1,
        "name": "John Smith",
        "phone": "79991234567",
        "comment": "Friend",
    }


def test_contact_from_dict() -> None:
    data = {
        "id": 1,
        "name": "John Smith",
        "phone": "79991234567",
        "comment": "Friend",
    }

    contact = Contact.from_dict(data)

    assert contact.id == 1
    assert contact.name == "John Smith"
    assert contact.phone == "79991234567"
    assert contact.comment == "Friend"


def test_contact_str() -> None:
    contact = Contact(
        1,
        "John Smith",
        "79991234567",
        "Friend"
    )

    result = str(contact)

    assert "ID: 1" in result
    assert "Name: John Smith" in result
    assert "Phone: 79991234567" in result
    assert "Comment: Friend" in result


def test_generate_id_for_empty_phonebook() -> None:
    phonebook = PhoneBook()

    assert phonebook.generate_id() == 1


def test_generate_id_for_existing_contacts() -> None:
    phonebook = PhoneBook()

    phonebook.add_contact(
        "John",
        "79991234567",
        "Test"
    )

    phonebook.add_contact(
        "Mike",
        "79161234567",
        "Test"
    )

    assert phonebook.generate_id() == 3


def test_generate_id_after_non_sequential_ids() -> None:
    phonebook = PhoneBook()

    contacts = [
        Contact(1, "John", "79991234567", "Test"),
        Contact(5, "Mike", "79161234567", "Test"),
        Contact(10, "Alex", "79991234567", "Test"),
    ]

    phonebook.load_contacts(contacts)

    assert phonebook.generate_id() == 11


def test_load_contacts_into_phonebook() -> None:
    phonebook = PhoneBook()

    contacts = [
        Contact(1, "John", "79991234567", "Friend"),
        Contact(2, "Mike", "79161234567", "Work"),
    ]

    phonebook.load_contacts(contacts)

    result = phonebook.get_all_contacts()

    assert len(result) == 2
    assert result[0].name == "John"
    assert result[1].name == "Mike"


def test_save_contacts(tmp_path) -> None:
    file_manager = FileManager()

    filename = tmp_path / "contacts.json"

    contacts = [
        Contact(
            1,
            "John Smith",
            "79991234567",
            "Friend"
        )
    ]

    file_manager.save_contacts(
        str(filename),
        contacts
    )

    assert filename.exists()


def test_load_contacts(tmp_path) -> None:
    file_manager = FileManager()

    filename = tmp_path / "contacts.json"

    contacts = [
        Contact(
            1,
            "John Smith",
            "79991234567",
            "Friend"
        )
    ]

    file_manager.save_contacts(
        str(filename),
        contacts
    )

    loaded_contacts = file_manager.load_contacts(
        str(filename)
    )

    assert len(loaded_contacts) == 1
    assert loaded_contacts[0].name == "John Smith"
    assert loaded_contacts[0].phone == "79991234567"


def test_save_and_load_contacts(tmp_path) -> None:
    file_manager = FileManager()

    filename = tmp_path / "contacts.json"

    contacts = [
        Contact(
            1,
            "John Smith",
            "79991234567",
            "Friend"
        ),
        Contact(
            2,
            "Mike Brown",
            "79161234567",
            "Work"
        ),
    ]

    file_manager.save_contacts(
        str(filename),
        contacts
    )

    loaded_contacts = file_manager.load_contacts(
        str(filename)
    )

    assert len(loaded_contacts) == 2
    assert loaded_contacts[0].to_dict() == contacts[0].to_dict()
    assert loaded_contacts[1].to_dict() == contacts[1].to_dict()


def test_load_nonexistent_file(tmp_path) -> None:
    file_manager = FileManager()

    filename = tmp_path / "not_exists.json"

    result = file_manager.load_contacts(
        str(filename)
    )

    assert result == []


def test_load_invalid_json(tmp_path) -> None:
    file_manager = FileManager()

    filename = tmp_path / "invalid.json"

    filename.write_text(
        "invalid json",
        encoding="utf-8"
    )

    with pytest.raises(FileReadError):
        file_manager.load_contacts(
            str(filename)
        )


def test_save_contacts_to_invalid_path() -> None:
    file_manager = FileManager()

    contacts = [
        Contact(
            1,
            "John Smith",
            "79991234567",
            "Friend"
        )
    ]

    with pytest.raises(FileWriteError):
        file_manager.save_contacts(
            "Z:/invalid_folder/contacts.json",
            contacts
        )