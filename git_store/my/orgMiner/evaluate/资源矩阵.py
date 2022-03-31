
# 从rl文件中获取资源矩阵
def _resource_matrix(rl_file):
    # 生成rl
    rl = csv_to_dataFrame(rl_file)
    # 获取profile
    profiles = get_profile(rl)
    resource_matrix = []
    for indexs in profiles.index:
        resource_matrix.append(profiles.loc[indexs].values[0:])
    return resource_matrix


def csv_to_dataFrame(file):
    import csv
    import pandas as pd
    tmp_lst = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
    return df


def get_profile(rl):
    # 生成profile
    from orgminer.ResourceProfiler.raw_profiler import count_execution_frequency
    profiles = count_execution_frequency(rl, scale=None)
    return profiles




if __name__ == "__main__":

    # 生成资源矩阵到文件中
    rl_p = '../数据/rl/'
    rl_file = ['bpic15_1_rl', 'bpic15_2_rl','bpic15_3_rl','bpic15_4_rl','bpic15_5_rl']
    end = '.csv'

    out_p='../数据/资源矩阵/'


    for i in range(len(rl_file)):
        resource_matrix=_resource_matrix(rl_p+rl_file[i]+end)
        with open(out_p+'01_'+rl_file[i]+end,
                  'w', newline='') as write_file:
            import csv
            writer = csv.writer(write_file)
            writer.writerows(resource_matrix)


