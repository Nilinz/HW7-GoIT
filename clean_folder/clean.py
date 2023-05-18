import os
import shutil
import zipfile
# Список категорій
known = {
    "archives": ["zip", "rar", "7z", "gz", "tar"],
    "video": ["mp4", "avi", "mkv", "mov"],
    "audio": ["mp3", "wav", "flac", "ogg", "amr"],
    "documents": ["docx", "xlsx", "pptx", "pdf", "txt", "doc"],
    "images": ["jpg", "jpeg", "png", "bmp", "gif"]
    
}

known_extensions = {}
unknown_extensions = []


def unpack_archives(directory):
    """Функція, яка рекурсивно розпаковує всі архіви у вказаній директорії та переміщує їх вміст до папки archives"""
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            # якщо це архів, розпаковуємо його в папку archives
            if item.endswith(".zip"):
                with zipfile.ZipFile(item_path, 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(directory, 'archives', os.path.splitext(item)[0]))
                os.remove(item_path)
        elif os.path.isdir(item_path):
            # якщо це папка, рекурсивно викликаємо функцію unpack_archives
            if item != 'archives':
                unpack_archives(item_path)

def normalize(filename):
    # транслітерація кириличних символів на латиницю
    table = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 
             'з': 'z', 'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 
             'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 
             'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ю': 'iu', 'я': 'ia', 'А': 'A', 'Б': 'B', 'В': 'V', 
             'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'IE', 'Ж': 'ZH', 'З': 'Z', 'И': 'Y', 'І': 'I', 
             'Ї': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 
             'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 
             'Щ': 'SHCH', 'Ю': 'IU', 'Я': 'IA'}
    for key, value in table.items():
        filename = filename.replace(key, value)
    

    # заміна всіх символів, крім літер латинського алфавіту та цифр, на символ '_'
    normalized_name = ''
    for letter in filename:
        if letter.isalnum():
            normalized_name += letter
        else:
            normalized_name += '_'
    return normalized_name

# Функція, що додає розширення до списку
def add_extension(extension):
    if extension in known_extensions:
        return
    if extension in unknown_extensions:
        unknown_extensions.remove(extension)
    else:
        known_extensions.add(extension)


def sort_files(path, base_path=None):
    known = {
    "archives": ["zip", "rar", "7z", "gz", "tar"],
    "video": ["mp4", "avi", "mkv", "mov"],
    "audio": ["mp3", "wav", "flac", "ogg", "amr"],
    "documents": ["docx", "xlsx", "pptx", "pdf", "txt", "doc"],
    "images": ["jpg", "jpeg", "png", "bmp", "gif"]
    }
    
    if base_path is None:
        base_path = path
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            if filename in ["archives", "video", "audio", "documents", "images"]:
                continue
            sort_files(filepath, base_path=base_path)
        else:
            extension = os.path.splitext(filename)[1][1:].lower()
            added = False
            for category, extensions in known.items():
                for ext in extensions:
                    known_extensions.setdefault(category, []).append(ext)
                    # known_extensions.append(ext)
                if extension in extensions:
                    category_path = os.path.join(base_path, category)
                    if not os.path.exists(category_path):
                        os.makedirs(category_path)
                    shutil.move(filepath, os.path.join(category_path, filename))
                    added = True
                    if category not in known_extensions:
                        known_extensions[category] = []
                    known_extensions[category].append(extension)
                    break
            if not added:
                unknown_extensions.append(extension)
    return known_extensions, unknown_extensions

def main():
    directory = input("Enter directory path: ")
    sort_files(directory, base_path=None)
    add_extension(extension)
    normalize(filename)
    unpack_archives(directory)


# if __name__ == "__main__":
#     main()

                        
if __name__ == '__main__':
    directory = input("Enter directory path: ")
    if os.path.isdir(directory):
        sort_files(directory)
    else:
        print("Invalid directory path.")
    unpack_archives(directory)            



for category in known:
    category_path = os.path.join(directory, category)
    if os.path.exists(category_path):
        print(f"\n{category.upper()}:\n")
        for filename in os.listdir(category_path):
            print(f"{normalize(filename)}")

print("Known extensions: ", known_extensions)
print("Unknown extensions: ", unknown_extensions)
