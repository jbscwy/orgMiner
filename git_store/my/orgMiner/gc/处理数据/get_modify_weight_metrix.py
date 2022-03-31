
# 计算每个资源组中每个执行模式被选中的概率
def get_modify_weight_metrix(num_group,profiles,execution_mode_group,full_matrix,ogs):
    from 处理数据.get_data_resources_by_profile import get_data_resources_by_profile
    dataset_list, resource_group = get_data_resources_by_profile(profiles)
    labels=get_labels(ogs, resource_group)
    weight_matrix, sums=get_weight_matrix(num_group,dataset_list, resource_group, execution_mode_group,full_matrix,labels)
    import copy
    wm=copy.deepcopy(weight_matrix)
    for i in range(len(wm)):
        before = 0
        for j in range(len(wm[0])):
            if wm[i][j]!=0:
                wm[i][j]=before+wm[i][j]/sums[i]
                before=wm[i][j]
    return wm



# 获取资源组标签
def get_labels(ogs,resource_group):
    labels=[0 for col in range(len(resource_group))]
    for i in range(len(ogs)):
        for og in ogs[i]:
            for k in range(len(resource_group)):
                if resource_group[k]==og:
                    labels[k]=i
                    break
    return labels


# 计算资源组中每个执行模式对该资源组的权重,生成相应的矩阵
def get_weight_matrix(num_group,dataset_list, resource_group, execution_mode_group,full_matrix,labels):
    # 初始化
    weight_matrix=[[0 for col in range(len(execution_mode_group))] for row in range(num_group)]
    sums=[]
    for i in range(len(full_matrix)):
        sum=0
        for j in range(len(full_matrix[0])):
            if full_matrix[i][j]>0:
                weight_matrix[i][j]=calculate_weight(i,j,dataset_list,resource_group,full_matrix,labels)
                sum=sum+weight_matrix[i][j]
        sums.append(sum)

    return weight_matrix,sums



# 计算单个资源组的单个执行模式的权重,权重越大，越可能发生变异
def calculate_weight(i,j,dataset_list,resource_group,full_matrix,labels):
    resource_map={}
    for l1 in range(len(resource_group)):
        resource_map[resource_group[l1]]=l1
    # resourses=om.find_group_members(i)
    resourses=[]
    for l in range(len(labels)):
        if labels[l]==i:
            resourses.append(resource_group[l])
    # 计算资源组中资源拥有该执行模式的比例
    n1=0
    m1=0
    for resourse in resourses:
        if dataset_list[resource_map[resourse]][j]>0:
            n1=n1+1
            m1=m1+dataset_list[resource_map[resourse]][j]
    M1=0
    for l2 in range(len(full_matrix[0])):
        M1=M1+full_matrix[i][l2]

    n2=0
    m2=0
    for resourse1 in resource_group:
        if resourse1 not in resourses and dataset_list[resource_map[resourse1]][j]>0:
            n2=n2+1
            m2=m2+dataset_list[resource_map[resourse1]][j]
    M2=0
    for l3 in range(len(full_matrix)):
        if l3 !=i:
            for l4 in range(len(full_matrix[0])):
                M2=M2+full_matrix[l3][l4]
    c = m1 / M1
    a = n1 / len(resourses)
    d=m2/M2
    b=n2/(len(resource_group)-len(resourses))

    X=(a-b)/(b+1)
    Y=(c-d)/(d+1)
    # import math
    E=(X+1)*(Y+1)
    return E
