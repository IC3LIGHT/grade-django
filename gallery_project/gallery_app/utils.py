import datetime as dt
import requests
from PIL import Image
import io
from django.core.files.uploadedfile import SimpleUploadedFile


def compare_date(date):
    json_date = requests.get('http://worldtimeapi.org/api/timezone/Europe/London').json()
    date_api = json_date['datetime'][:10]
    date_list = date_api.split('-')
    current_str = f'{date_list[2]}.{date_list[1]}.{date_list[0]}'
    cur_date = dt.datetime.strptime(current_str, '%d.%m.%Y')
    try:
        user_date = dt.datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        return "Некорректная дата."
    print(cur_date)
    print(user_date)
    if user_date > cur_date:
        return False
    else:
        return True


def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def is_valid_date(date):
    try:
        day, month, year = map(int, date.split('.'))
    except ValueError:
        return "Некорректная дата."

    if year < 1 or month < 1 or month > 12 or day < 1:
        return False

    if month in [1, 3, 5, 7, 8, 10, 12]:
        return day <= 31
    elif month in [4, 6, 9, 11]:
        return day <= 30
    elif month == 2:
        if is_leap_year(year):
            return day <= 29
        else:
            return day <= 28

    return False



def generate_phone_number():
    import random
    number = "+7"
    for _ in range(10):
        number += str(random.randint(0, 9))
    return number


def create_test_image():
    # Создание изображения
    image = Image.new('RGB', (100, 100), color='red')
    image_file = io.BytesIO()
    image.save(image_file, format='JPEG')
    image_file.name = 'test.jpg'
    image_file.seek(0)

    return SimpleUploadedFile(image_file.name, image_file.read(), content_type='image/jpeg')