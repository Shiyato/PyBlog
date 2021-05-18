from datetime import datetime
from PIL import Image
from db_models import Post
import re
import os


def justify_text(text:str):

    text_strings = re.split(r'\n', text)
    for i in range(len(text_strings)):
        text_strings[i] = f'<p>{text_strings[i]}</p>'

    return '\n'.join(text_strings)




def pic_change_name(before, after):
    photos_path = os.path.abspath('static/images/users_photos')
    before = f'{photos_path}/{before}'
    after = f'{photos_path}/{after}'

    img = Image.open(before)
    img.save(after)
    if os.path.exists(before) and os.path.exists(after):
        os.remove(before)


def timedelta_to_datetime(delta):
    tld = delta.days
    years = tld // 365
    months = tld % 365 // 30
    days = tld % 30

    tls = delta.seconds
    hours = tls // 3600
    minutes = tls % 3600 // 60
    seconds = tls % 60

    rt = {'hour':int(hours), 'minute':int(minutes), 'second':int(seconds), 'day':int(days), 'month':int(months), 'year':int(years)}
    for key in rt.keys():
        if rt[key] < 0:
            rt[key] = 0
    return rt

def time_format(time:datetime):
    now = datetime.utcnow()
    delta = now - time
    delta = timedelta_to_datetime(delta)

    def word_form(num:int):
        rt = 0
        if num < 10 or num > 20:
            if num % 10 == 1:
                rt = 1
            elif num % 10 in (2, 3, 4):
                rt = 2
            else:
                rt = 3
        else:
            rt = 3
        return rt

    if delta['day']:
        if delta['year']:
            n = delta['year']
            form = ('год', 'года', 'лет')
            rt = f'{n} {form[word_form(n) - 1]}'
        elif delta['month']:
            n = delta['month']
            form = ('месяц', 'месяца', 'месяцев')
            rt = f'{n} {form[word_form(n) - 1]}'
        elif delta['day'] >= 7:
            n = delta['day'] // 7
            form = ('неделю', 'недели', 'недель')
            rt = f'{n} {form[word_form(n) - 1]}'
        else:
            n = delta['day']
            form = ('день', 'дня', 'дней')
            rt = f'{n} {form[word_form(n) - 1]}'
    else:
        if delta['hour']:
            n = delta['hour']
            form = ('час', 'часа', 'часов')
            rt = f'{n} {form[word_form(n) - 1]}'
        elif delta['minute']:
            n = delta['minute']
            form = ('минуту', 'минуты', 'минут')
            rt = f'{n} {form[word_form(n) - 1]}'
        else:
            n = delta['second']
            form = ('секунду', 'секунды', 'секунд')
            rt = f'{n} {form[word_form(n) - 1]}'

    return rt
