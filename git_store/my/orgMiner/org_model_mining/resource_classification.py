# This Python file uses the following encoding: utf-8
# 将案例类型、活动类型、时间类型合并成执行模式
import csv
def make_execution__mode(file):
    data=open(file)
    next(data)
    dataset=[]
    head=['resource','execution_mode']
    dataset.append(head)
    ds=[]
    for e in data:
        e=e.replace('\n','').replace('\r','').split(',')
        ds.append(e[0])
        ds.append(e[1] + "|" + e[2] + "|" + e[3])
        dataset.append(ds.copy())
        ds.clear()
    return dataset


# get resource log
def derive_resource_log(r_file):
    data=open(r_file)
    next(data)
    rl=[]
    # rl.append()
    for line in data:
        line = line.replace('\n', '').replace('\r', '').split(',')
        print(line)
        if line[0] is not None and line[0]!='':
            rl.append({
                'resource': line[0],
                'case_type': line[1],
                'activity_type': line[2],
                'time_type': line[3]
            })

    from pandas import DataFrame
    rl=DataFrame(rl)
    print('Resource Log derived: ',end='')
    print('{} events mapped onto {} execution modes.\n'.format(
        len(data.readlines()),
        len(rl.drop_duplicates(
            subset=['case_type', 'activity_type', 'time_type'],
            inplace=False))
    ))
    return rl



# 生成资源组和执行模式组
def get_resource_group_and_execution_mode_group(file):
    data=open(file)
    next(data)
    resource_group=[]
    execution_mode_group=[]
    for e in data:
        e = e.replace('\n','').replace('\r','').split(',')
        resource=e[0]
        execution_mode=e[1]+"|"+e[2]+"|"+e[3]
        if resource not in resource_group:
            resource_group.append(resource)
        if execution_mode not in execution_mode_group:
            execution_mode_group.append(execution_mode)
    return resource_group,execution_mode_group


# 生成资源特征矩阵
def reource_feature_matrix(dataset,reource_group,execution_mode_group):
    N=[]
    for i in range(len(reource_group)):
        N.append([0]*len(execution_mode_group))
    row=0
    col=0
    for data in dataset[1:]:
        for i in range(len(reource_group)):
            if reource_group[i]==data[0]:
                row=i
                break
        for j in range(len(execution_mode_group)):
            if execution_mode_group[j]==data[1]:
                col=j
                break
        N[row][col]=N[row][col]+1
    return N

# 闵可夫斯基距离公式(欧式公式)
import numpy as np
def Euclidean_distance(X,Y):
    v1=np.mat(X)
    v2=np.mat(Y)
    return np.sqrt((v1-v2)*(v1-v2).T)

# 汉明公式
def hammingDistance(X,Y):
    l=len(X)
    hamming_distance=0
    for i in range(l):
        if X[i]!=Y[i]:
            hamming_distance=hamming_distance+1
    return hamming_distance

# 皮尔逊相关系数
def pearson_r(X,Y):
    mx=np.mean(X,axis=0)
    my=np.mean(Y,axis=0)
    xm,ym=X-mx,Y-my
    r_num=np.sum(xm*ym)
    x_square_sum=np.sum(xm*xm)
    y_square_sum=np.sum(ym*ym)
    r_den=np.sqrt(x_square_sum*y_square_sum)
    r=r_num/r_den
    return np.mean(r)

# 空间相似性
def spatial_difference(X,Y):
    s=0
    l=len(X)
    for i in range(l):
        s+=1/(1+abs(X[i]-Y[i]))
    return s/l


# 夹角余弦
def cosine(X,Y):
    cosV12=np.dot(X,Y)/(np.linalg.norm(X)*np.linalg.norm(Y))
    return cosV12


if __name__ == '__main__':
    x=[2,0,0,0,0,0,0]
    y=[0,1,0,0,0,0,0]
    X=np.vstack([x,y])
    from scipy.spatial.distance import pdist
    d2=pdist(X)
    print(d2)








