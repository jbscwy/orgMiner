def ogs_to_labels(ogs,resources):
    labels=[-1 for col in range(len(resources))]
    for i in range(len(resources)):
        for j in range(len(ogs)):
            if resources[i] in ogs[j]:
                labels[i]=j
    return labels