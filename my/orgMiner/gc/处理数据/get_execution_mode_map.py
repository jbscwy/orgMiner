def get_execution_mode_map(profiles):
    execution_mode_group = []
    for index in profiles.columns:
        execution_mode_group.append(index)
    # 从组织模型中获取每组中存在的资源和执行模式
    execution_mode_map = {}
    for i in range(len(execution_mode_group)):
        execution_mode_map[execution_mode_group[i]] = i
    return execution_mode_map