def AHC(profiles, num_group):
    from orgminer.OrganizationalModelMiner.clustering.hierarchical \
        import _ahc
    ogs, og_hcy = _ahc(profiles, num_group, method='single', metric='euclidean')
    resources = get_resources(profiles)
    labels=ogs_to_labels(ogs,resources)
    return labels


def get_resources(profiles):
    resource_group = []
    for i, r in enumerate(sorted(profiles.index)):
        resource_group.append(r)
    return resource_group







def ogs_to_labels(ogs,resources):
    labels=[-1 for col in range(len(resources))]
    for i in range(len(resources)):
        for j in range(len(ogs)):
            if resources[i] in ogs[j]:
                labels[i]=j
    return labels


