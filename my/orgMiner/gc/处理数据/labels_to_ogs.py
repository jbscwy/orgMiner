# 获取挖掘后的分组
def labels_to_ogs(resource_group,labels):
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