import csv

from my.orgMiner.resource_log.activity_type import activity_type
from my.orgMiner.resource_log.time_type import get_time_type

# model_file="../.event/GoogleNews-vectors-negative300.bin"
# 读取csv日志
import pandas as pd

def read_csv_event_log(file,resource_column):
    data=pd.read_csv(file)
    list_data=data.values.tolist()
    l=len(list_data)
    event_log=[]
    for i in range(l):
        if list_data[i][resource_column]=='nan':
            continue
        event_log.append(list_data[i])
    return event_log


# 将事件日志转化为资源日志主函数
def event_to_resource(fn_event_log,fout_res_log,resource_column,case_type_column,activity_column,
                      activity_type_method,timestamp_column,timestamp_format,time_type_method,is_frequency='0',frequency_range=[],
                      activities_groups_number='3',model_file="../.event/GoogleNews-vectors-negative300.bin"):
    resource_log = []
    activities_groups_number=int(activities_groups_number)
    resource_column=int(resource_column)
    case_type_column=int(case_type_column)
    activity_column=int(activity_column)
    timestamp_column=int(timestamp_column)
    attrs = ['resource', 'case_type', 'activity_type', 'time_type']
    dataset = read_csv_event_log(fn_event_log, resource_column)


    resources=[]
    cases_type=[]
    activities_type=[]
    times_type=[]
    activities=[]
    timestamps=[]
    for line in dataset:
        resource=line[resource_column]
        case_type=line[case_type_column]
        activity=line[activity_column]
        timestamp=line[timestamp_column]
        resources.append(resource)
        cases_type.append(case_type)
        activities.append(activity)
        timestamps.append(timestamp)

    # 获取资源
    # 获取案例类型
    # 获取活动类型
    if activity_type_method=='0':
        activities_type=activities
    elif activity_type_method=='1':
        # 这里添加基于活动名聚类
        activities_type=activity_type(activities, model_file, activities_groups_number)
    # 获取时间类型
    times_type=get_time_type(timestamps,time_type_method,timestamp_format,is_frequency,frequency_range)

    resources_size=len(resources)
    case_type_size=len(cases_type)
    activity_type_size=len(activities_type)
    times_type_size=len(times_type)
    if resources_size==case_type_size and case_type_size== activity_type_size and activity_type_size==times_type_size:
        for i in range(resources_size):
            resource_event=[]
            resource_event.append(resources[i])
            resource_event.append(cases_type[i])
            resource_event.append(activities_type[i])
            resource_event.append(times_type[i])
            resource_log.append(resource_event)


    with open(fout_res_log+'.csv', 'w', newline='') as t:
        writer = csv.writer(t)
        writer.writerow(attrs)
        writer.writerows(resource_log)







if __name__ == '__main__':
    # 将事件日志转化为资源日志
    fn_event_log = '../.event/running-example-non-conforming.csv'
    fout_res_log = '../.event/resource'
    resource_line = '4'
    case_type_column = '5'
    activity_column = '3'
    # 是否进行活动聚类
    activity_type_method='1'
    activities_groups_number = '3'
    timestamp_column= '2'
    time_type_method = '2'
    is_frequency='1'
    frequency_range=['10','20']

    timestamp_format = '%d-%m-%Y:%H.%M'
    event_to_resource(fn_event_log, fout_res_log, resource_line, case_type_column, activity_column,
                      activity_type_method, timestamp_column,timestamp_format,time_type_method, is_frequency, frequency_range,
                      activities_groups_number)
