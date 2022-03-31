from sklearn.cluster import _k_means


def K_means(profiles,n_groups):
    from sklearn.cluster import KMeans
    labels = KMeans(n_clusters=n_groups).fit_predict(profiles)
    return labels


def get_resources(profiles):
    resource_group = []
    for i, r in enumerate(sorted(profiles.index)):
        resource_group.append(r)
    return resource_group


# 获取挖掘后的分组
def get_ogs(resource_group,labels):
    # 将资源组用frozenset存储
    resource_data = [labels, resource_group]
    resource_data = list(map(list, zip(*resource_data)))
    from pandas import DataFrame
    import numpy as np
    rd = DataFrame(np.array(resource_data), columns=['label', 'resource'])
    ogs = list()
    for label, event in rd.groupby("label"):
        ogs.append(frozenset(event['resource']))
    return ogs