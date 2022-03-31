


def KFCM(rl_file,num_group):
    from 处理数据.csv_to_dataFrame import csv_to_dataFrame
    rl = csv_to_dataFrame(rl_file)
    from orgminer.ResourceProfiler.raw_profiler import count_execution_frequency
    profiles = count_execution_frequency(rl, scale=None)
    from 处理数据.get_data_resources_by_profile import get_data_resources_by_profile
    dataset_list, resource_group = get_data_resources_by_profile(profiles)
    centers = init_centers_by_k_means(profiles, num_group, dataset_list, resource_group)
    from B资源分组.fcm import _fcm
    labels = _fcm(profiles, num_group, centers, 2)
    return labels


def init_centers_by_k_means(profiles,cluster_number,dataset_list,resource_group):
    from orgminer.OrganizationalModelMiner.clustering.hierarchical import _ahc
    ogs, og_hcy = _ahc(profiles, cluster_number, method='single', metric='euclidean')
    centers = []
    for og in ogs:
        sum = [0 for col in range(len(dataset_list[0]))]
        for i in range(len(resource_group)):
            if resource_group[i] in og:
                sum += dataset_list[i]
        for j in range(len(sum)):
            sum[j] = sum[j] / len(og)
        centers.append(sum)
    return centers