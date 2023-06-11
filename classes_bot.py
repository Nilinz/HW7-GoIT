from collections import UserDict

class Field:
    def __init__(self):
        self.value = None

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__()
        self.value = name

class Phone(Field):
    def __init__(self, phone):
        super().__init__()
        self.value = phone

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

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
def add_contact(name, phone):
    if name.isdigit():
        return "Invalid input. Name should be a text."
    if name in contacts:
        record = contacts[name]
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
    return "Contact added successfully."

@input_error
def change_contact(name, phone):
    if name.isdigit():
        return "Invalid input. Name should be a text."
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
        for record in contacts.values():
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
        elif command == "show all":
            print(show_all_contacts())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
