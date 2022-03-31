import csv
import logging
from collections import OrderedDict

import gensim
from gensim.models import word2vec
import numpy as np





model_file="../.event/GoogleNews-vectors-negative300.bin"
# 加载模型
def load_model(model_file):
    model=gensim.models.KeyedVectors.load_word2vec_format(model_file,binary=True)
    return model


# 读取活动列,去重
def read_active_column(file,activity_column):
    activities = set()
    with open(file, 'r') as csvfile:
        next(csvfile)
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            activities.add(row[activity_column])
    return activities

# 再次读取活动列,不去重,并生成活动类型
def get_active_type(file,activity_column,group_dic):
    activity_types=[]
    with open(file,'r') as csvfile:
        next(csvfile)
        csvreader=csv.reader(csvfile)
        for row in csvreader:
            for key,value in group_dic.items():
                if row[activity_column] in value:
                    activity_types.append(key)
    return activity_types


# 将活动类型转化
def get_activity_type(activities,group_dic):
    for i in range(len(activities)):
        for key,value in group_dic.items():
            if activities[i] in value:
                activities[i]=key
    return activities






# 获取每个(活动名,向量)的字典表示
def activity_vector(activitys,model):
    acitivity_dic=dict()
    for activity_name in activitys:
       activity_name_matrix= get_activity_name_matrix(activity_name,model)
       acitivity_dic[activity_name]=activity_name_matrix
    return acitivity_dic

# 将活动名用向量表示
def get_activity_name_matrix(activity_name,model):
    sentences_matrix=[]
    word_list=activity_name.split()
    for word in word_list:
        sentences_matrix.append(np.array(model[word]))
    # 对数组取平均值
    if len(sentences_matrix)==1:
        return sentences_matrix
    result=averageVector(sentences_matrix)
    return result


# 取多个向量的平均值
def averageVector(many_vectors):
    result=[]
    row=len(many_vectors)
    col=len(many_vectors[0])
    for c in range(col):
        sum=0.0
        for r in range(row):
            sum+=many_vectors[r][c]
        result.append(sum/col)
    return result

# 凝聚层次聚类,根据活动名相似性聚类
def AHC(acitivity_dic,k):
    groups=[]
    for key in acitivity_dic.keys():
        list=[]
        list.append(key)
        groups.append(list)

    # 计算每个点对之间的距离
    simP2P={}
    for key1,value1 in acitivity_dic.items():
        for key2,value2 in acitivity_dic.items():
            if key1!=key2:
                sim=cosine_similarity(value1,value2)
                simP2P[str(key1)+"#"+str(key2)]=sim
    # 按相似度升序将各个点对排序
    simP2P=OrderedDict(sorted(simP2P.items(),key=lambda t:t[1]))
    # 当前有的簇个数
    groupNum=len(groups)
    while groupNum>k:
        # 选取下一个距离最近的点
        twopoints,similarity=simP2P.popitem()
        pointA=twopoints.split('#')[0]
        pointB=twopoints.split('#')[1]
        pointA_location=get_point_location(pointA,groups)
        pointB_location = get_point_location(pointB, groups)
        if pointA_location != pointB_location:
            merge_array(groups,pointA_location,pointB_location)
            print(str(groups))
            groupNum-=1
    group_dic={}
    for i in range(len(groups)):
        key="activity_type"+str(i)
        group_dic[key]=groups[i]
    return group_dic



# 合并二维数组中指定两个数组
def merge_array(groups, i, j):
    groups[i].extend(groups[j])
    groups.pop(j)

# 获取活动在活动组中的位置
def get_point_location(activity,groups):
    for i in range(len(groups)):
        if activity in groups[i]:
            return i
    return -1

# 余弦相似度计算
def cosine_similarity(vector_a,vector_b):
    vector_a=np.mat(vector_a)
    vector_b=np.mat(vector_b)
    num=float(vector_a*vector_b.T)
    denom=np.linalg.norm(vector_a)*np.linalg.norm(vector_b)
    cos=num/denom
    sim=0.5+0.5*cos
    return sim

# 将活动去重
def activities_heavy(activities):
    new_activities=set()
    for activity in activities:
        new_activities.add(activity)
    return new_activities

def activity_type(activities,model_file,k):
    # 活动字段去重
    new_activities=activities_heavy(activities)
    # 加载模型
    model=load_model(model_file)
    # 获取每个（活动名，向量）的字典表示,若活动名由多个字段组成，取向量的平均值
    activity_dic=activity_vector(activities,model)
    # 使用AHC算法对活动聚类，获得活动分类情况
    group_dic = AHC(activity_dic, k)
    # 再次读取活动字段（不去重）,获取活动类型字段,以数组形式保存
    activity_types = get_activity_type(activities, group_dic)
    return activity_types





# the main program of mining activity type
def mining_activity_type(log_file,model_file,activity_column,k):
    # 读取活动字段（去重）
    activities=read_active_column(log_file,activity_column)
    # 加载模型
    model=load_model(model_file)
    # 获取每个（活动名，向量）的字典表示
    acitivity_dic=activity_vector(activities,model)
    # 使用AHC算法对活动聚类，获得活动分类情况
    group_dic=AHC(acitivity_dic, k)
    # 再次读取活动字段（不去重）,获取活动类型字段,以数组形式保存
    activity_types=get_active_type(log_file, activity_column, group_dic)
    return activity_types



if __name__ == '__main__':
    log_file = "../.event/Test2.csv"
    model_file = "../.event/GoogleNews-vectors-negative300.bin"
    activity_column = 2
    k = 3
    activity_types = mining_activity_type(log_file, model_file, activity_column, k)
    print(activity_types)