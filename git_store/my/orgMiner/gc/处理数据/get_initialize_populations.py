# 读取csv文件获取资源组执行模式矩阵
def get_initialize_populations(file_path):
    # 读取文件夹中所有csv文件
    from os import listdir
    files = sorted(fn for fn in listdir(file_path) if fn.endswith('.csv'))
    # 依次读取文件中数据
    initialize_populations=[]
    for i, fn in enumerate(files):
        import numpy
        from os.path import join
        initialize_population = numpy.loadtxt(open(join(file_path,fn), "rb"),dtype=int, delimiter=",", skiprows=0)
        initialize_populations.append(initialize_population)
    return initialize_populations