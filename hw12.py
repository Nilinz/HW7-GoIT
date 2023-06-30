import datetime
import re
from collections import UserDict
import pickle


class Field:
    def __init__(self):
        self._value = None

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return repr(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __init__(self, name):
        super().__init__()
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        super().__init__()
        self.value = phone

    @Field.value.setter
    def value(self, new_value):
        if not self._is_valid_phone(new_value):
            raise ValueError("Invalid phone number.")
        self._value = new_value

    def _is_valid_phone(self, phone):
        if len(phone) != 6:
            return False
        if not phone.isdigit():
            return False
        return True


class Birthday(Field):
    def __init__(self, birthday=None):
        super().__init__()
        if birthday:
            self.value = self._parse_birthday(birthday)
        else:
            self.value = None

    @Field.value.setter
    def value(self, new_value):
        if new_value and not self._is_valid_birthday(new_value):
            raise ValueError("Invalid birthday.")
        self._value = new_value

    def _is_valid_birthday(self, birthday):
        try:
            datetime.datetime.strptime(str(birthday), "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _parse_birthday(self, birthday):
        return datetime.datetime.strptime(str(birthday), "%Y-%m-%d").date()


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def get_next_birthday(self, current_year):
        today = datetime.date.today()
        current_year_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)

        if current_year_birthday >= today:
            return current_year_birthday
        else:
            next_year_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            return next_year_birthday

    def days_to_birthday(self):
        if self.birthday.value:
            next_birthday = self.get_next_birthday(datetime.date.today().year)
            days_left = (next_birthday - datetime.date.today()).days
            return days_left
        return None


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def save_to_disk(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def load_from_disk(self, filename):
        with open(filename, "rb") as file:
            self.data = pickle.load(file)


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input."
        except IndexError:
            return "Invalid input."

    return wrapper


contacts = AddressBook()


@input_error
def add_contact(name, phone=None, birthday=None):
    if name.isdigit():
        return "Invalid input. Name should be text."
    if name in contacts:
        record = contacts[name]
        if phone:
            record.add_phone(phone)
        if birthday:
            record.birthday.value = birthday
    else:
        record = Record(name, birthday)
        if phone:
            record.add_phone(phone)
        contacts.add_record(record)
    return "Contact added successfully."


@input_error
def change_contact(name, phone):
    if name.isdigit():
        return "Invalid input. Name should be text."
    if name in contacts:
        record = contacts[name]
        record.edit_phone(record.phones[0].value, phone)
        return "Contact updated successfully."
    else:
        return "Contact not found."


@input_error
def get_phone_number(name):
    if name in contacts:
        record = contacts[name]
        return record.phones[0].value
    else:
        return "Contact not found."


def show_all_contacts():
    if len(contacts) == 0:
        return "No contacts found."
    else:
        result = ""
        for record in contacts.data.values():
            phones = ", ".join(str(phone) for phone in record.phones)
            result += f"{record.name}: {phones}\n"
        return result.strip()


def main():
    filename = "address_book.pkl"  # ім'я файлу для збереження адресної книги

    try:
        contacts.load_from_disk(filename)  # спроба завантаження адресної книги з диска
        print("Address book loaded from disk.")
    except FileNotFoundError:
        print("No address book found on disk.")

    print("Hello! My commands: add, change, phone, show all. You can type the command like this: add JohnDoe 123456 1990-05-15. To finish type close or exit.")
    while True:
        command = input("> ").lower()

        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone, birthday = command.split(" ", 3)
            print(add_contact(name, phone, birthday))
        elif command.startswith("change"):
            _, name, phone = command.split(" ", 2)
            print(change_contact(name, phone))
        elif command.startswith("phone"):
            _, name = command.split(" ", 1)
            print(get_phone_number(name))
        elif command == "show all":
            print(show_all_contacts())
        elif command == "save":
            contacts.save_to_disk(filename)  # зберегти адресну книгу на диск
            print("Address book saved to disk.")
        elif command == "exit":
            contacts.save_to_disk(filename)  # зберегти адресну книгу на диск перед виходом
            print("Address book saved to disk.")
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
