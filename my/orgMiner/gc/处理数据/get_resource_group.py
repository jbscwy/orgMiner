def get_resource_group(profiles):
    resource_group = []
    for i, r in enumerate(sorted(profiles.index)):
        resource_group.append(r)
    return resource_group