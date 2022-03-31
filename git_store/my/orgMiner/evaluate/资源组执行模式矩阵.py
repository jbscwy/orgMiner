# 已知：01资源组执行模式矩阵、资源矩阵、labels
# 求：资源组执行模式矩阵


# 获取资源组执行模式矩阵
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


# 读取文件中矩阵
def get_matrix_by_file(matrix_file):
    import numpy
    group_matrix = numpy.loadtxt(open(matrix_file, "rb"), dtype=int, delimiter=",", skiprows=0)
    return group_matrix


def get_labels_by_file(ogs_file):
    labels = []
    with open(ogs_file, 'r') as f:
        import csv
        reader = csv.reader(f)
        for row in reader:
            for i in range(len(row)):
                labels.append(int(row[i]))
    return labels

# 读取文件夹中所有矩阵
def get_matrixs_by_folder(folder_path):
    # 读取文件夹中所有csv文件
    from os import listdir
    files = sorted(fn for fn in listdir(folder_path) if fn.endswith('.csv'))
    # 依次读取文件中数据
    matrixs = []
    for i, fn in enumerate(files):
        import numpy
        from os.path import join
        matrix = numpy.loadtxt(open(join(folder_path, fn), "rb"), dtype=int, delimiter=",", skiprows=0)
        matrixs.append(matrix)
    return matrixs





if __name__ == "__main__":
    # 读取01资源组执行模式矩阵
    resource_group_matrix_p_p='../数据/01资源组执行模式矩阵/'
    logs=['1/','2/','3/','4/','5/']
    resource_group_methods=['ahc','k_means','AFCM','KFCM']

    # 读取资源矩阵
    resource_matrix_p='../数据/资源矩阵/'
    resource_matrix_file=['bpic15_1_rm','bpic15_2_rm','bpic15_3_rm','bpic15_4_rm','bpic15_5_rm']
    end='.csv'

    # 读取labels
    resource_labels_p='../数据/资源分组_labels/'
    ahc_labels=['bpic15_1_ahc_17_labels',
                'bpic15_2_ahc_6_labels',
                'bpic15_3_ahc_9_labels',
                'bpic15_4_ahc_5_labels',
                'bpic15_5_ahc_16_labels']
    k_means_labels=['bpic15_1_rl.csvk_means_k=17_labels',
                    'bpic15_2_rl.csvk_means_k=6_labels',
                    'bpic15_3_rl.csvk_means_k=9_labels',
                    'bpic15_4_rl.csvk_means_k=5_labels',
                    'bpic15_5_rl.csvk_means_k=17_labels']
    AFCM_labels=['bpic15_1_rl.csv_FCM_ahc_k=16_labels',
                 'bpic15_2_rl.csv_FCM_ahc_k=6_labels',
                 'bpic15_3_rl.csv_FCM_ahc_k=9_labels',
                 'bpic15_4_rl.csv_FCM_ahc_k=5_labels',
                 'bpic15_5_rl.csv_FCM_ahc_k=16_labels']
    KFCM_labels=['bpic15_1_rl.csv_FCM_k_means_k=16_labels',
                 'bpic15_2_rl.csv_FCM_k_means_k=6_labels',
                 'bpic15_3_rl.csv_FCM_k_means_k=9_labels',
                 'bpic15_4_rl.csv_FCM_k_means_k=5_labels',
                 'bpic15_5_rl.csv_FCM_k_means_k=17_labels']

    out_p='../数据/资源组执行模式矩阵/'

    # 获取资源组执行模式矩阵
    for i in range(len(logs)):
        # 读取资源矩阵
        resource_matrix=get_matrix_by_file(resource_matrix_p+resource_matrix_file[i]+end)
        # 遍历资源分组方法
        for resource_group_method in resource_group_methods:
            # 读取labels
            if resource_group_method == 'ahc':
                labels = get_labels_by_file(resource_labels_p +resource_group_method+'/'+ ahc_labels[i]+end)
            elif resource_group_method == 'k_means':
                labels = get_labels_by_file(resource_labels_p +resource_group_method+ '/'+k_means_labels[i]+end)
            elif resource_group_method=='AFCM':
                labels=get_labels_by_file(resource_labels_p+resource_group_method+'/'+AFCM_labels[i]+end)
            else:
                labels = get_labels_by_file(resource_labels_p +resource_group_method+'/'+ KFCM_labels[i]+end)
            # 获取日志和资源分组方法对应的所有01资源组执行模式矩阵
            resource_group_matrixs=get_matrixs_by_folder(resource_group_matrix_p_p+logs[i]+resource_group_method)
            # 生成资源组执行模式矩阵
            for resource_group_matrix in resource_group_matrixs:
                after_resource_group_matrix=_after_resource_group_matrix(resource_group_matrix, resource_matrix, labels)
                with open(out_p+logs[i]+resource_group_method+'/'+resource_matrix_file[i]+'_'+resource_group_method+'_after_resource_group_matrix'+end,
                          'w', newline='') as write_file:
                    import csv
                    writer = csv.writer(write_file)
                    writer.writerows(after_resource_group_matrix)



