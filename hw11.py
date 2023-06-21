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
        if not self._is_valid_phone(new_value):
            raise ValueError("Invalid phone number.")
        self._value = new_value

    def _is_valid_phone(self, phone):
        # Перевірка на коректність номера телефону
        # Реалізуйте свою власну логіку перевірки тут
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
        # Перевірка на коректність дня народження
        # Реалізуйте свою власну логіку перевірки тут
        return True

    def _parse_birthday(self, birthday):
        # Парсинг дня народження і повернення об'єкта datetime.date
        # Реалізуйте свою власну логіку парсингу тут
        return datetime.date.today()


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
        if self.birthday.value:
            today = datetime.date.today()
            next_birthday = self._get_next_birthday(today.year)
            days_left = (next_birthday - today).days
            return days_left
        return None

    def _get_next_birthday(self, current_year):
        # Отримання дати наступного дня народження на підставі поточного року
        # Реалізуйте свою власну логіку тут
        return datetime.date(current_year, 1, 1)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return iter(self.data.values())


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
        return "Invalid input. Name should be text."
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
        for record in contacts:
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
        elif command == "days to birthday":
            _, name = command.split(" ", 1)
            if name in contacts:
                record = contacts[name]
                days_left = record.days_to_birthday()
                if days_left:
                    print(f"Days to {name}'s birthday: {days_left}")
                else:
                    print(f"{name} doesn't have a birthday recorded.")
            else:
                print("Contact not found.")
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()