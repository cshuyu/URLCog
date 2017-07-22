import time

time_arr = time.strptime('2010-08-22', "%Y-%m-%d")
timeStamp = str(int(time.mktime(time_arr)))
print(timeStamp)