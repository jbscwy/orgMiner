def get_resource_group_matrix(om, dataset_list, profiles):
    execution_mode_group = []
    for index in profiles.columns:
        execution_mode_group.append(index)
    # 从组织模型中获取每组中存在的资源和执行模式
    execution_mode_map = {}
    for i in range(len(execution_mode_group)):
        execution_mode_map[execution_mode_group[i]] = i


    resource_group_execution_mode = []
    for j in range(om.group_number):
        # 第i组中的资源
        import numpy
        rgem = numpy.array([0 for col in range(len(dataset_list[0]))])
        # gm=om.find_group_members(j)
        # # 第i组中拥有的执行模式
        gem = om.find_group_execution_modes(j)
        for em in gem:
            print(em)
            rgem[execution_mode_map[em]] = 1
        resource_group_execution_mode.append(rgem)
    return resource_group_execution_mode