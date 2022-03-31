def get_data_resources_by_profile(profiles):
    dataset_list = []
    for indexs in profiles.index:
        dataset_list.append(profiles.loc[indexs].values[0:])
    resource_group = []
    for i, r in enumerate(sorted(profiles.index)):
        resource_group.append(r)
    return dataset_list,resource_group