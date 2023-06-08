contacts = {}

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

def add_contact(name, phone):
    if name.isdigit():
        return "Invalid input. Name should be a text."
    contacts[name] = phone
    return "Contact added successfully."

def change_contact(name, phone):
    if name.isdigit():
        return "Invalid input. Name should be a text."
    contacts[name] = phone
    return "Contact updated successfully."

def get_phone_number(name):
    return contacts[name]

def show_all_contacts():
    if len(contacts) == 0:
        return "No contacts found."
    else:
        result = ""
        for name, phone in contacts.items():
            result += f"{name}: {phone}\n"
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
