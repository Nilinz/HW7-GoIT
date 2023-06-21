import datetime
from collections import UserDict

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
            raise ValueError("Phone number should only contain digits.")
        self._value = new_value

class Birthday(Field):
    def __init__(self, birthday=None):
        super().__init__()
        self.value = birthday

    @Field.value.setter
    def value(self, new_value):
        if new_value is not None:
            try:
                datetime.datetime.strptime(new_value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid birthday format. Please use YYYY-MM-DD.")
        self._value = new_value

    def days_to_birthday(self):
        if self.value is None:
            return None

        today = datetime.date.today()
        next_birthday_year = today.year
        next_birthday = datetime.datetime.strptime(
            f"{next_birthday_year}-{self.value[5:]}",
            "%Y-%m-%d"
        ).date()

        if today > next_birthday:
            next_birthday_year += 1
            next_birthday = datetime.datetime.strptime(
                f"{next_birthday_year}-{self.value[5:]}",
                "%Y-%m-%d"
            ).date()

        return (next_birthday - today).days

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

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 5

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, page=1):
        total_pages = len(self) // self.page_size + 1
        page = max(1, min(page, total_pages))
        start = (page - 1) * self.page_size
        end = start + self.page_size
        records = list(self.data.values())[start:end]
        return records

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

def add_contact(name, phone, birthday=None):
    if name.isdigit():
        return "Invalid input. Name should be a text."
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
        return "Invalid input. Name should be a text."
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

def show_all_contacts(page=1):
    if len(contacts) == 0:
        return "No contacts found."
    else:
        result = ""
        records = contacts.iterator(page)
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
            _, name, phone, *birthday = command.split(" ", 3)
            print(add_contact(name, phone, *birthday))
        elif command.startswith("change"):
            _, name, phone = command.split(" ", 2)
            print(change_contact(name, phone))
        elif command.startswith("phone"):
            _, name = command.split(" ", 1)
            print(get_phone_number(name))
        elif command.startswith("show all"):
            if len(command.split()) > 2:
                _, page = command.split(" ", 2)
                print(show_all_contacts(int(page)))
            else:
                print(show_all_contacts())
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
 
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
