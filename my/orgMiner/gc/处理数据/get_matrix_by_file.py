# 读取文件中矩阵
def get_matrix_by_file(matrix_file):
    import numpy
    group_matrix = numpy.loadtxt(open(matrix_file, "rb"), dtype=int, delimiter=",", skiprows=0)
    return group_matrix