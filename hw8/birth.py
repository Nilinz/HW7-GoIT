import datetime

def get_birthdays_per_week(users):
    # Отримуємо поточну дату
    today = datetime.date.today()
    
    # Знаходимо день тижня, з якого починається поточний тиждень (понеділок)
    start_of_week = today - datetime.timedelta(days=today.weekday())
    
    # Знаходимо дату, на яку закінчується поточний тиждень (неділя)
    end_of_week = start_of_week + datetime.timedelta(days=6)
    
    # Фільтруємо користувачів, які мають день народження на поточному тижні
    birthdays_this_week = [user for user in users if start_of_week <= user['birthday'].date() <= end_of_week]
    
    # Створюємо словник, де ключ - день тижня, а значення - список користувачів
    birthdays_by_day = {}
    
    # Додаємо користувачів до відповідного дня тижня
    for user in birthdays_this_week:
        birthday_date = user['birthday'].date()
        birthday_day = birthday_date.strftime('%A')  # Отримуємо назву дня тижня
        if birthday_day not in birthdays_by_day:
            birthdays_by_day[birthday_day] = []
        birthdays_by_day[birthday_day].append(user['name'])
    
    # Виводимо список користувачів по днях тижня
    if birthdays_by_day:
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            if day in birthdays_by_day:
                print(f'{day}: {", ".join(birthdays_by_day[day])}')
    else:
        print("Немає користувачів для привітання на цьому тижні.")


users = [
    {'name': 'Bill', 'birthday': datetime.datetime(2023, 5, 26)},
    {'name': 'Jill', 'birthday': datetime.datetime(2023, 6, 2)},
    {'name': 'Kim', 'birthday': datetime.datetime(2023, 6, 3)},
    {'name': 'Jan', 'birthday': datetime.datetime(2023, 6, 4)}
]

get_birthdays_per_week(users)
