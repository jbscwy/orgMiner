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