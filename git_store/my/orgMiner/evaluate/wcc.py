# 已知：资源分组（资源矩阵、01资源矩阵）、分配执行模式（资源组执行模式矩阵、01资源组执行模式矩阵）
# 计算资源的轮廓系数平均值
def _wcc(labels,resource_matrix,after_resource_matrix,resource_group_matrix,after_resource_group_matrix):
    sum=0
    for i in range(len(resource_matrix)):
        a=_a(i, labels, resource_matrix, after_resource_matrix)
        # 计算各资源组之间的距离
        gg_distance=_gg_distance(resource_group_matrix, after_resource_group_matrix)
        # 计算当前资源组与最近资源组之间的距离
        b=_b(i, gg_distance,labels)
        if max(a,b)==0.0:
            c=0
        else:
            c=(b-a)/max(a,b)
        sum=sum+c
    return sum/len(resource_matrix)


# 更改wcc
def _change_wcc(wcc):
    return (wcc+1)/2




# 计算两资源的距离
def a_distance1(r1,r2):
    s1=0
    for i in range(len(r1)):
        import math
        s1=s1+math.fabs(r1[i]-r2[i])
    return s1


def a_distance2(af1,af2):
    s2=0
    for i in range(len(af1)):
        import math
        s2 = s2 + math.fabs(af1[i] - af2[i])
    return s2


# 计算资源组内单个资源与其他资源的平均距离
def _a(i,labels,resource_execution_matrix,after_resource_matrix):
    sum=0
    n=0
    for j in range(len(labels)):
        if labels[i]==labels[j]:
            sum=sum+a_distance1(resource_execution_matrix[i],resource_execution_matrix[j])
            sum=sum+a_distance2(after_resource_matrix[i],after_resource_matrix[j])
            sum=sum/2
            n=n+1
    return sum/n


# 计算两资源的距离
def b_distance1(g1,g2):
    s1=0
    for i in range(len(g1)):
        import math
        s1=s1+math.fabs(g1[i]-g2[i])
    return s1


def b_distance2(ag1,ag2):
    s2=0
    for i in range(len(ag1)):
        import math
        s2 = s2 + math.fabs(ag1[i] - ag2[i])
    return s2


# 计算各资源组之间的距离，并存到二维数组中
def _gg_distance(group_execution_matrix,after_group_matrix):
    gg_distance = [[0 for col in range(len(group_execution_matrix))] for row in range(len(group_execution_matrix))]
    for i in range(len(group_execution_matrix)):
        distance = 0
        for j in range(len(group_execution_matrix)):
            distance = distance + b_distance1(group_execution_matrix[i], group_execution_matrix[j])
            distance = distance + b_distance2(after_group_matrix[i], after_group_matrix[j])
            distance = distance / 2
            gg_distance[i][j] = distance
    return gg_distance


# 计算当前资源与最近资源组中资源的平均距离
def _b(i,gg_distance,labels):
    # 获取与当前资源组最近的资源组
    import sys
    closest=sys.maxsize
    for j in range(len(gg_distance[labels[i]])):
        if labels[i]!=j and closest>gg_distance[labels[i]][j]:
            closest=gg_distance[labels[i]][j]
    return closest
