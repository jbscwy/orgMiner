# 获取执行模式组
def get_execution_mode_group(profiles):
    execution_mode_group = []
    for index in profiles.columns:
        execution_mode_group.append(index)
    return execution_mode_group