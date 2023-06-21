from collections import UserDict
from datetime import datetime, timedelta

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
        if not new_value.isdigit():
            raise ValueError("Invalid phone number.")
        self._value = new_value

class Birthday(Field):
    def __init__(self, birthday=None):
        super().__init__()
        self.value = birthday

    @Field.value.setter
    def value(self, new_value):
        if new_value is not None:
            try:
                datetime.strptime(new_value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid birthday format. Please use YYYY-MM-DD.")
        self._value = new_value

    def days_to_birthday(self):
        if self.value:
            today = datetime.today()
            birthday = datetime.strptime(self.value, "%Y-%m-%d")
            next_birthday = datetime(today.year, birthday.month, birthday.day)
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, birthday.month, birthday.day)
            days = (next_birthday - today).days
            return days

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

    def days_to_birthday(self):
        return self.birthday.days_to_birthday()

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self._index = 0
        self._page_size = 5

    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        records = list(self.data.values())
        if self._index < len(records):
            start = self._index
            self._index += self._page_size
            return records[start:self._index]
        raise StopIteration

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Invalid input."
    return wrapper

contacts = AddressBook()

def add_contact(name, phone, birthday=None):
    if name.isdigit():
        return "Invalid input. Name should be text."
    if name in contacts:
        record = contacts[name]
        record.add_phone(phone)
    else:
        record = Record(name, birthday)
        record.add_phone(phone)
        contacts.add_record(record)
    return "Contact added successfully."

def change_contact(name, phone):
    if name.isdigit():
        return "Invalid input. Name should be text."
    if name in contacts:
        record = contacts[name]
        record.edit_phone(record.phones[0].value, phone)
        return "Contact updated successfully."
    else:
        return "Contact not found."

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
        for records in contacts:
            for record in records:
                phones = ", ".join(str(phone) for phone in record.phones)
                result += f"{record.name}: {phones}\n"
        return result.strip()

def main():
    print("Hello! My commands: add, change, phone, show all. Type contact name without a space. Example: add MarkoMark 138238932832. To finish type close or exit.")
    while True:
        command = input("> ").lower()
        
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone = command.split(" ", 2)
            print(add_contact(name, phone))
        elif command.startswith("change"):
            _, name, phone = command.split(" ", 2)
            print(change_contact(name, phone))
        elif command.startswith("phone"):
            _, name = command.split(" ", 1)
            print(get_phone_number(name))
        elif command.startswith("days"):
            _, name = command.split(" ", 1)
            if name in contacts:
                record = contacts[name]
                days = record.days_to_birthday()
                if days is None:
                    print("Birthday is not set for this contact.")
                else:
                    print(f"Days to birthday: {days}")
            else:
                print("Contact not found.")
        elif command == "show all":
            print(show_all_contacts())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
