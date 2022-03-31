


def _01_resource_matrix(resource_matrix_file):
    resource_matrix=get_resource_matrix_by_file(resource_matrix_file)
    for i in range(len(resource_matrix)):
        for j in range(len(resource_matrix[0])):
            if resource_matrix[i][j]>0:
                resource_matrix[i][j]=1
    return resource_matrix


# 读取资源文件中资源矩阵
def get_resource_matrix_by_file(resource_matrix_file):
    import numpy
    group_matrix = numpy.loadtxt(open(resource_matrix_file, "rb"), dtype=int, delimiter=",", skiprows=0)
    return group_matrix


if __name__ == "__main__":
    resource_matrix_p = '../数据/资源矩阵/'
    resource_matrix_file = ['bpic15_1_rm', 'bpic15_2_rm', 'bpic15_3_rm', 'bpic15_4_rm', 'bpic15_5_rm']
    end = '.csv'
    out_p='../数据/01资源矩阵/'
    for i in range(len(resource_matrix_file)):
        after_resource_matrix=_01_resource_matrix(resource_matrix_p+resource_matrix_file[i]+end)
        with open(out_p+'01_'+resource_matrix_file[i]+end,
                  'w', newline='') as write_file:
            import csv
            writer = csv.writer(write_file)
            writer.writerows(after_resource_matrix)


