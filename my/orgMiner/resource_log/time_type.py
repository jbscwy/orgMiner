import re
import numpy as np
from datetime import datetime
import csv
# 从案例中读取时间类型





# 读取时间戳字段
def get_time_stamp(file,time_column):
    timestamps=[]
    with open(file, 'r') as csvfile:
        next(csvfile)
        csvreader = csv.reader(csvfile)
        for line in csvreader:
            timestamps.append(line[time_column])
    return timestamps

# 按时间层次修改时间戳字段
def time_level_division(timestamps,time_level,timestamp_format):
    timestamps1=[]
    for i in range(len(timestamps)):
        time_type=one_timestamp_amend(timestamps[i],time_level,timestamp_format)
        timestamps1.append(time_type)
    return timestamps1

# 字典格式保存按频率划分时间段的结果
def dictionary_save(timestamps,frequency_range=[]):
    low_frequency=int(frequency_range[0])
    high_frequency=int(frequency_range[1])
    time_dic={}
    for timestamp in timestamps:
        if timestamp not in time_dic.keys():
            time_dic[timestamp]=1
        else:
            time_dic[timestamp]+=1
    for key,value in time_dic.items():
        if value<low_frequency:
            time_dic[key]="free"
        elif value>high_frequency:
            time_dic[key]="busy"
        else:
            time_dic[key]="normal"
    return time_dic

# 按频率修改时间字段
def frequency_division(timestamps,frequency_range=[]):
    time_dic=dictionary_save(timestamps, frequency_range)
    for i in range(len(timestamps)):
        for key,value in time_dic.items():
            if key==timestamps[i]:
                timestamps[i]=value
    return timestamps


# 将时间戳转化为日志格式
def timestamp_to_format(timestamp=None,format = '%Y-%m-%d %H:%M:%S'):
    # try:
    if timestamp:
        time_tuple = time.localtime(timestamp)
        #print('type(time_tuple):',type(time_tuple))
        res = time.strftime(format,time_tuple)
    else:
        res = time.strftime(format)
    return res


import re
import numpy as np
from datetime import datetime
import time
# 单个时间戳字段修改
def one_timestamp_amend(timestamp, i,timestamp_format='%Y-%m-%d %H:%M:%S'):
    if timestamp_format != '%Y-%m-%d %H:%M:%S':
        time_tuple = time.strptime(timestamp, timestamp_format)  # 把格式化好的时间转换成元祖
        result = time.mktime(time_tuple)  # 把时间元祖转换成时间戳
        timestamp = timestamp_to_format(result)
    time_type = timestamp
    if i == '0':  # 表示时间类型以年为单位,修改对应的时间类型
        time_type = timestamp[0:4]
    if i == '2':  # 表示时间类型以月为单位，修改对应的时间类型
        time_type = timestamp[6:7]
    if i == '5':  # 表示时间类型以小时为单位，修改对应的时间类型
        time_type = timestamp[12:13]
    if i == '1':  # 表示时间类型以季度为单位，修改对应的时间类型
        d1 = int(timestamp[6:7])
        if d1 in [1, 2, 3]:
            time_type = 1
        if d1 in [4, 5, 6]:
            time_type = 2
        if d1 in [7, 8, 9]:
            time_type = 3
        if d1 in [10, 11, 12]:
            time_type = 4
    if i == '3':  # 表示时间类型以星期为单位，修改对应的时间类型
        time1 = re.search(r"\d{4}-\d{1,2}-\d{1,2}", str(timestamp)).group(0)
        ts = time1.split('-')
        arr = np.array(ts)
        s = ''.join(arr)
        week = datetime.strptime(s, "%Y%m%d").weekday() + 1
        time_type = week
    if i == '4':  # 按早中晚来区分时间
        hour = timestamp[12:13]
        try:
            h = int(hour)
        except:
            print("格式异常")

        if int(hour) >= 6 and int(hour) < 12:
            time_type = 'morning'
        if int(hour) >= 12 and int(hour) < 18:
            time_type = 'afternoon'
        if int(hour) >= 18 and int(hour) <= 24:
            time_type = 'evening'
        if int(hour) >= 0 and int(hour) < 6:
            time_type = 'evening'
    return time_type


# 挖掘时间类型主程序
def get_time_type(timestamps,time_level,timestamp_format,is_frequency_division='0',frequency_range=[]):
    # 按时间层次修改时间戳字段
    timestamps=time_level_division(timestamps,time_level,timestamp_format)
    # 按时间频率再次修改时间戳字段
    if is_frequency_division=='1':
        timestamps=frequency_division(timestamps,frequency_range)
    return timestamps

if __name__ == '__main__':
    log_file='../.event/running-example-non-conforming.csv'
    time_column=2
    time_level='3'
    is_frequency_division='1'
    frequency_range=[5,10]
    # 读取日志中时间戳字段
    ts=get_time_stamp(log_file,time_column)
    # timestamp_format = '%Y-%m-%d %H:%M:%S'
    timestamp_format = '%d-%m-%Y:%H.%M'
    timestamps=get_time_type(ts, time_level,timestamp_format, is_frequency_division, frequency_range)
    print(timestamps)
