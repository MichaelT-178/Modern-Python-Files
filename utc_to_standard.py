"""
Converts UTC time to Eastern Standard time.

Input: 1705194520
Ouput: EST: Saturday, January 13, 2024 8:08:40 PM
"""

import datetime
from termcolor import colored as c

utc_time = int(input("Enter UTC time (Ex. 1705194520): "))

dt_utc = datetime.datetime.fromtimestamp(utc_time, tz=datetime.timezone.utc)
dt_est = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=-5)))


# print(f"{c("UTC:", 'magenta')} {dt_utc.strftime("%B %d, %Y %I:%M:%S %p")}")

print(f"{c("EST:", 'green')} {dt_est.strftime("%A, %B %d, %Y %-I:%M:%S %p")}")
