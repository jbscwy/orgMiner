# 已知：资源分组（资源矩阵(resource_matrix)、分组(labels)）、分配执行模式（01资源组执行模式矩阵(resource_group_matrix)）
# 计算：01资源矩阵（after_resource_matrix）、资源组执行模式矩阵（after_resource_group_matrix）






# 从文件中获取labels
def _labels(labels_file):
    labels = []
    with open(labels_file, 'r') as f:
        import csv
        reader = csv.reader(f)
        for row in reader:
            for i in range(len(row)):
                labels.append(int(row[i]))
    return labels


# 从文件夹中获取01资源组执行模式矩阵
def _resource_group_matrix(file_path):
    # 读取文件夹中所有csv文件
    from os import listdir
    files = sorted(fn for fn in listdir(file_path) if fn.endswith('.csv'))
    # 依次读取文件中数据
    resource_group_matrixs = []
    for i, fn in enumerate(files):
        import numpy
        from os.path import join
        resource_group_matrix = numpy.loadtxt(open(join(file_path, fn), "rb"), dtype=int, delimiter=",", skiprows=0)
        resource_group_matrixs.append(resource_group_matrix)
    return resource_group_matrixs





# 01资源矩阵
def _after_resource_matrix(resource_matrix):
    import copy
    after_resource_matrix=copy.copy(resource_matrix)
    for i in range(len(after_resource_matrix)):
        for j in range(len(after_resource_matrix[i])):
            if after_resource_matrix[i][j]>0:
                after_resource_matrix[i][j]=1
    return after_resource_matrix



# 两个数组相加
def add_array(a,b):
    for i in range(len(a)):
        a[i]=a[i]+b[i]
    return a

# 两个矩阵相乘
def multiply_matrix(copy_resource_group_matrix,rgm):
    full_resource_group_matrix=[[0 for col in range(len(copy_resource_group_matrix[0]))] for row in range(len(copy_resource_group_matrix))]
    for i in range(len(copy_resource_group_matrix)):
        for j in range(len(copy_resource_group_matrix[0])):
            full_resource_group_matrix[i][j]=copy_resource_group_matrix[i][j]*rgm[i][j]
    return full_resource_group_matrix



# 资源组执行模式矩阵
def _after_resource_group_matrix(resource_group_matrix,resource_matrix,labels):
    # 获取全分配执行组执行模式矩阵
    import copy
    copy_resource_group_matrix = copy.copy(resource_group_matrix)
    rgm = [[0 for col in range(len(resource_group_matrix[0]))] for row in range(len(resource_group_matrix))]
    for rg in range(len(resource_group_matrix)):
        for i in range(len(labels)):
            if rg == labels[i]:
                add_array(rgm[rg], resource_matrix[i])
    # 两个矩阵相乘
    full_resource_group_matrix = multiply_matrix(copy_resource_group_matrix, rgm)
    return full_resource_group_matrix








