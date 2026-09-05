class PhoneBookError(Exception):
    """Base exception for the phonebook."""


class ContactNotFoundError(PhoneBookError):
    """Raised when a contact cannot be found."""


class InvalidContactError(PhoneBookError):
    """Raised when contact data is invalid."""


class InvalidPhoneError(PhoneBookError):
    """Raised when a phone number is invalid."""


class FileReadError(PhoneBookError):
    """Raised when a file cannot be read."""


class FileWriteError(PhoneBookError):
    """Raised when a file cannot be written."""