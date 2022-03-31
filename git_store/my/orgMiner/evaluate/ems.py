def _ems(labels,resource_matrix,resource_group_matrix):
    ems=resource_execution_mode_similarity(labels, resource_matrix, resource_group_matrix)
    return ems


# 资源执行模式相似性
def resource_execution_mode_similarity(labels,resource_execution_matrix,group_matrix):
    sum=0
    for i in range(len(resource_execution_matrix)):
        rm=resource_execution_matrix[i]
        gm=group_matrix[labels[i]]
        rm_n=0
        gm_n=0
        rgm_n=0
        for j in range(len(rm)):
            if rm[j]==1:
                rm_n+=1
            if gm[j]==1:
                gm_n+=1
            if rm[j]==1 and gm[j]==1:
                rgm_n+=1
        sum+=rgm_n*2/(rm_n+gm_n)
    res=sum/len(labels)
    return res


# 获取labels
def get_labels_by_file(ogs_file):
    labels = []
    with open(ogs_file, 'r') as f:
        import csv
        reader = csv.reader(f)
        for row in reader:
            for i in range(len(row)):
                labels.append(int(row[i]))
    return labels


# 获取资源执行模式矩阵,并修改成0，1的形式
def get_resource_execution_matrix(profiles):
    resource_execution_matrix = []
    for indexs in profiles.index:
        resource_execution_matrix.append(profiles.loc[indexs].values[0:])
    for i in range(len(resource_execution_matrix)):
        for j in range(len(resource_execution_matrix[0])):
            if resource_execution_matrix[i][j]>0:
                resource_execution_matrix[i][j]=1
    return resource_execution_matrix


# 读取csv文件获取资源组执行模式矩阵
def get_group_matrixs(file_path):
    # 读取文件夹中所有csv文件
    from os import listdir
    files = sorted(fn for fn in listdir(file_path) if fn.endswith('.csv'))
    # 依次读取文件中数据
    group_matrixs=[]
    for i, fn in enumerate(files):
        import numpy
        from os.path import join
        group_matrix = numpy.loadtxt(open(join(file_path,fn), "rb"),dtype=int, delimiter=",", skiprows=0)
        group_matrixs.append(group_matrix)
    return group_matrixs







