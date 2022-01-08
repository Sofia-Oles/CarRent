import datetime


def change_time(date):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    t = datetime.time(hour=9, minute=00)
    return datetime.datetime.combine(yesterday, t)


def prepare_to_service(data):
    data_to_validate = dict()
    for key, value in data.items():
        if value and key != "csrf_token" and key != "submit":
            data_to_validate[key] = value
    return data_to_validate
