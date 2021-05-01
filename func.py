from datetime import datetime

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
    print('now', now)
    print('time', time)
    delta = now - time
    print('delta', delta)
    delta = timedelta_to_datetime(delta)
    print('delta', delta)

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
            rt = f'{n} {form[word_form(n) - 1]} назад'
        elif delta['month']:
            n = delta['month']
            form = ('месяц', 'месяца', 'месяцев')
            rt = f'{n} {form[word_form(n) - 1]} назад'
        elif delta['day'] >= 7:
            n = delta['day'] // 7
            form = ('неделя', 'недели', 'недель')
            rt = f'{n} {form[word_form(n) - 1]} назад'
        else:
            n = delta['day']
            form = ('день', 'дня', 'дней')
            rt = f'{n} {form[word_form(n) - 1]} назад'
    else:
        if delta['hour']:
            n = delta['hour']
            form = ('час', 'часа', 'часов')
            rt = f'{n} {form[word_form(n) - 1]} назад'
        elif delta['minute']:
            n = delta['minute']
            form = ('минута', 'минуты', 'минут')
            rt = f'{n} {form[word_form(n) - 1]} назад'
        else:
            n = delta['second']
            form = ('секунда', 'секунды', 'секунд')
            rt = f'{n} {form[word_form(n) - 1]} назад'

    return rt