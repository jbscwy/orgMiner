from my.orgMiner.org_model_mining.assign_execution_modes import string_to_list


def fitness(event_log, om):
    event_log_size = len(event_log) - 1
    conf_size = 0
    for i in range(1, len(event_log)):
        for key, value in om.items():
            resource_group = string_to_list(key)
            if event_log[i][0] in resource_group and event_log[i][1] in value:
                conf_size += 1
    ft = round(conf_size / event_log_size, 3)
    return ft


# 允许事件数
def allow_events(om, event_log):
    size = 0
    for event in event_log[1:]:
        for value in om.values():
            if event[1] in value:
                size += 1
                continue
    return size


# 候选资源总数
def all_candidate_resouces(om):
    candidate_list = []
    for key, value in om.items():
        resource_group = string_to_list(key)
        for resource in resource_group:
            if resource in candidate_list:
                continue
            else:
                candidate_list.append(resource)
    return candidate_list


# 一致性事件数
def conforming_events(event_log, om):
    conf_event = []
    size = 0
    for event in event_log[1:]:
        for key, value in om.items():
            resource_group = string_to_list(key)
            if event[0] in resource_group and event[1] in value:
                size += 1
                conf_event.append(event)
    return conf_event, size


# 某一事件对应的候选资源，可以理解为某一执行模式对应的候选资源
def candidate_resources(event, om):
    size = 0
    for key, value in om.items():
        resource_group = string_to_list(key)
        if event[1] in value:
            size += len(resource_group)
    return size


# 定义执行模式-资源的形式
def execution_mode_to_resource(om):
    em_to_re = {}
    for key, value in om.items():
        for em in value:
            if em not in em_to_re.keys():
                cand_groups = set(string_to_list(key))
                em_to_re[em] = cand_groups
            else:
                cand_groups = em_to_re[em]
                ls = string_to_list(key)
                for cand in ls:
                    cand_groups.add(cand)
                em_to_re[em] = cand_groups
    return em_to_re


#  判断是否为允许事件，
def _is_allowed_event(event, em_to_re):
    cand_groups = set()
    for key, value in em_to_re.items():
        if key == event[1]:
            for cand in value:
                cand_groups.add(cand)
                break
    return len(cand_groups) > 0


# 发现候选资源组
def find_candidate_groups(event, em_to_re):
    cand_groups = set()
    for key, value in em_to_re.items():
        if key == event[1]:
            for cand in value:
                cand_groups.add(cand)
            break
    return cand_groups


# 适合度
def _fitness(resource_log, om):
    n_conformed_event = 0
    n_events = len(resource_log) - 1
    for event in resource_log:
        for key, value in om.items():
            if event[1] in value:
                n_conformed_event += 1
                break
    return n_conformed_event / n_events


# 精确度(最终版)
def _precision(resource_log, om):
    cand_E = set()
    em_to_re = execution_mode_to_resource(om)
    for event in resource_log[1:]:
        # 判断事件是否是允许事件，
        if _is_allowed_event(event, em_to_re):
            # 发现该事件，即该执行模式的候选资源组
            cand_groups = find_candidate_groups(event, em_to_re)
            # 添加到总的候选资源集-cand_E中
            for cand in cand_groups:
                cand_E.add(cand)
    n_cand_E = len(cand_E)
    if n_cand_E == 0:
        return float('nan')
    else:
        n_allowed_events = 0
        precision = 0.0

        for event in resource_log[1:]:
            if _is_allowed_event(event, em_to_re):
                # 允许事件+1
                n_allowed_events += 1
                # 发现该事件的候选资源组
                cand_groups = find_candidate_groups(event, em_to_re)
                # 获取该事件的候选资源组长度
                n_cand_e = len(cand_groups)
                if _is_conformed_event(event, em_to_re):
                    precision += (n_cand_E + 1 - n_cand_e) / n_cand_E
                else:
                    precision += 0.0
        precision *= 1 / n_allowed_events
        return precision


# 判断是否是合格事件
def _is_conformed_event(event, em_to_re):
    cand_groups = find_candidate_groups(event, em_to_re)
    for g in cand_groups:
        if event[0] in g:
            return True
    return False


# 资源功能相似性度量
def resource_functional_Similarity(resource_log, om):
    rfs = 0.0
    r_em_in_log = resource_to_execute_model_in_log(resource_log)
    r_em_in_model = resource_to_execute_model_in_model(om)
    for key in r_em_in_log.keys():
        log_model_size, log_size, model_size = single_functional_similarity(key, r_em_in_log, r_em_in_model)
        rfs += (log_model_size * 2) / (log_size + model_size)
    rfs *= 1 / len(r_em_in_log)
    return rfs


# 计算某个资源在日志和组织模型中相似的功能数
def single_functional_similarity(resource, r_em_in_log, r_em_in_model):
    function_in_log = []
    function_in_model = []
    log_model_size = 0
    for key, value in r_em_in_log.items():
        if key == resource:
            function_in_log = value
            break
    log_size = len(function_in_log)
    for key, value in r_em_in_model.items():
        if key == resource:
            function_in_model = value
            break
    model_size = len(function_in_model)
    for function in function_in_log:
        if function in function_in_model:
            log_model_size += 1
    return log_model_size, log_size, model_size


# 将资源日志转化为资源 to 执行模式的形式
def resource_to_execute_model_in_log(resource_log):
    r_em_in_log = {}
    for event in resource_log[1:]:
        if event[0] not in r_em_in_log.keys():
            ems = set()
            ems.add(event[1])
            r_em_in_log[event[0]] = ems
        else:
            ems = r_em_in_log[event[0]]
            ems.add(event[1])
            r_em_in_log[event[0]] = ems
    return r_em_in_log


# 将组织模型转化为资源to执行模式的形式
def resource_to_execute_model_in_model(om):
    r_em_in_model = {}
    for key, value in om.items():
        resource_group = string_to_list(key)
        for resource in resource_group:
            r_em_in_model[resource] = value
    return r_em_in_model
