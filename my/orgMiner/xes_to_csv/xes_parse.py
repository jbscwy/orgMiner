# This Python file uses the following encoding: utf-8
# 逐行处理,用字典存储日志

log_dic = {}
attributes=[]

def dic_storage_log(file):
    fo = open(file, "r")
    flag1 = 0
    flag2 = 0
    dic_key = ''
    array_1 = []
    pro_list = []
    is_first_event = True
    attributes.append("trace:concept:name")
    for line in fo:
        t1 = '<trace>'
        if t1 in line:
            flag1 = 1
            continue
        t2 = '<string key="concept:name" value='
        if t2 in line and flag1 == 1 and flag2 == 0:
            key, value = get_key_and_value(line)
            dic_key = value
            continue
        e = '<event>'
        if e in line and flag1 == 1:
            flag2 = 1
            continue

        # 处理事件日志中的属性列
        p1 = '<string'
        if p1 in line and flag1 == 1 and flag2 == 1:
            key, value = get_key_and_value(line)
            if is_first_event == True:
                attributes.append(key)
            n=[key,value]
            pro_list.append(n)
            continue
        p2 = '<date'
        if p2 in line and flag1 == 1 and flag2 == 1:
            key, value = get_key_and_value(line)
            if is_first_event == True:
                attributes.append(key)
            if key == 'time:timestamp':
                value = time_format_conversion(value)
            n = [key, value]
            pro_list.append(n)
            continue
        p3 = '<int'
        if p3 in line and flag1 == 1 and flag2 == 1:
            key, value = get_key_and_value(line)
            if is_first_event == True:
                attributes.append(key)
            n = [key, value]
            pro_list.append(n)
            continue
        p4 = '<float'
        if p4 in line and flag1 == 1 and flag2 == 1:
            key, value = get_key_and_value(line)
            if is_first_event == True:
                attributes.append(key)
            n = [key, value]
            pro_list.append(n)
            continue
        p5 = '<boolean'
        if p5 in line and flag1 == 1 and flag2 == 1:
            key, value = get_key_and_value(line)
            if is_first_event == True:
                attributes.append(key)
            n = [key, value]
            pro_list.append(n)
            continue
        p6 = '<ID'
        if p6 in line and flag1 == 1 and flag2 == 1:
            key, value = get_key_and_value(line)
            if is_first_event == True:
                attributes.append(key)
            n = [key, value]
            pro_list.append(n)
            continue
        ed = '</event>'
        if ed in line and flag1 == 1:
            if is_first_event == True:
                is_first_event = False
            flag2 = 0
            array_1.append(pro_list.copy())
            pro_list.clear()
            continue
        td = '</trace>'
        if td in line:
            flag1 = 0
            log_dic[dic_key] = array_1.copy()
            array_1.clear()
            continue
    return attributes, log_dic



# 从字符串中获取key,value
def get_key_and_value(str):
    key_location = str.find('key=') + 5
    value_location = str.find('value=') + 7
    key = ''
    for char in str[key_location:]:
        if char != "\"":
            key = key + char
        else:
            break
    value = ''
    for char in str[value_location:]:
        if char != "\"":
            value = value + char
        else:
            break
    return key,value


# 获取字符串中某一字符位置
def get_location(str,char):
    l=len(str)
    for i in range(l):
        if str[i]==char:
            return int(i)
    return -1


import time
# 时间格式转换
def time_format_conversion(timestamp):
    local = get_location(timestamp, '+')
    timestamp = timestamp[0:local - 1]
    timeArray = time.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
    after_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return after_time

import csv
def generate_csv_file(file,attributes, log_dic={}):
    with open(file, 'w', newline='') as t:
        writer = csv.writer(t)
        writer.writerow(attributes)
        data = []
        data1 = [None]*len(attributes)
        for key, value in log_dic.items():
            for e in value:
                data1[0]=key
                for i in range(len(e)):
                    for j in range(len(attributes)):
                        if e[i][0]==attributes[j]:
                            data1[j]=(e[i][1])
                data.append(data1.copy())
                data1= [None]*len(attributes)
        writer.writerows(data)


if __name__ == '__main__':
    # print('Please enter a csv file:')
    # log = input()
    file = '..\.xes\eyJjc3JmX3Rva2VuIjoiMDY1ZmQ5NmQy.log.xes'
    attributes,log_dic=dic_storage_log(file)
    generate_csv_file('example',attributes,log_dic)








