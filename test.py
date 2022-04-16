import datetime

a = (datetime.datetime.now().date() - datetime.date(2022, 12, 12)).days
print(a < 0)