
def _ahc_labels(profiles,cluster_number,resource_group):
    from orgminer.OrganizationalModelMiner.clustering.hierarchical import _ahc
    ogs, og_hcy = _ahc(profiles, cluster_number, method='single', metric='euclidean')
    labels=ogs_to_labels(ogs, resource_group)
    return labels

def ogs_to_labels(ogs,resources):
    labels=[-1 for col in range(len(resources))]
    for i in range(len(resources)):
        for j in range(len(ogs)):
            if resources[i] in ogs[j]:
                labels[i]=j
    return labels


def get_resource_group(profiles):
    resource_group = []
    for i, r in enumerate(sorted(profiles.index)):
        resource_group.append(r)
    return resource_group



if __name__ == '__main__':

    rl_p = '../数据/rl/'
    rl_file = ['bpic15_1_rl', 'bpic15_2_rl', 'bpic15_3_rl', 'bpic15_4_rl', 'bpic15_5_rl']
    end = '.csv'
    cluster_numbers = [17, 6, 9, 5, 16]

    labels_file_p='../数据/资源分组_labels/ahc/'

    for i in range(len(rl_file)):
        # 生成rl
        from 处理数据.资源矩阵 import csv_to_dataFrame
        rl = csv_to_dataFrame(rl_p+rl_file[i]+end)
        # 获取profile
        from 处理数据.资源矩阵 import get_profile
        profile = get_profile(rl)
        # 从profile中获取资源
        resources=get_resource_group(profile)
        labels=_ahc_labels(profile, cluster_numbers[i], resources)
        with open(labels_file_p+rl_file[i]+'_'+str(cluster_numbers[i])+'_labels'+end,'w',newline='')as f:
            import csv
            mywrite=csv.writer(f)
            mywrite.writerow(labels)


