import sys
from datetime import datetime, timedelta, timezone

sys.path.append(".")

from models.time import Time
from models.interval import IntradayIntervalSeconds



def get_utcnow():
    now = datetime.now(timezone.utc)

    time = Time()
    time.Year = now.year
    time.Month = now.month
    time.Day = now.day
    time.Hour = now.hour
    time.Minute = now.minute
    time.Second = now.second
    time.Microsecond = now.microsecond
    time.Timestamp = int(now.timestamp())
    
    return time



def round_time(date_time = None, interval : IntradayIntervalSeconds = None):
    if interval is None : interval = IntradayIntervalSeconds._4h
    round_to = interval.value

    if date_time is None : date_time = datetime.now(timezone.utc)

    seconds = (date_time.replace(tzinfo = None) - date_time.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    new_datetime = date_time + timedelta(0, rounding - seconds, - date_time.microsecond)
    
    time = Time()
    
    time.Year = new_datetime.year
    time.Month = new_datetime.month
    time.Day = new_datetime.day
    time.Hour = new_datetime.hour
    time.Minute = new_datetime.minute
    time.Second = new_datetime.second
    time.Microsecond = new_datetime.microsecond
    time.Timestamp = int(new_datetime.timestamp())
    
    return time



# Test : OK
print("--------")

model = get_utcnow()
rounded_time = round_time(datetime.fromtimestamp(model.Timestamp))

print(rounded_time.Year)
print(rounded_time.Month)
print(rounded_time.Day)
print(rounded_time.Hour)
print(rounded_time.Minute)
print(rounded_time.Second)
print(rounded_time.Microsecond)
print(rounded_time.Timestamp)

print("--------")

# deprecated (!)
# print(datetime.utcnow())
