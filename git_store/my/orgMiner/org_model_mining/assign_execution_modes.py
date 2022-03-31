
def _fullRecall(after_resource_group=[],resource_execution_modes={}):
    dic={}
    afg_len = len(after_resource_group)
    for i in range(afg_len):
        k=after_resource_group[i]
        v=[]
        for j in range(len(after_resource_group[i])):
            for key,value in resource_execution_modes.items():
                if key is after_resource_group[i][j]:
                    for m in value:
                        if m in v:
                            continue
                        else:
                            v.append(m)
            dic[str(k)]=v.copy()
    return dic




# 整体核心法（OverallScore）,需要测量一个模式和一个资源组的相关程度
def overall_score(dataset=[],resources=[],execution_mode_group=[],after_resource_group=[],resource_execution_modes={},k1=0.8,k2=0.8):
    # 初始组织模型
    org_model=_fullRecall(after_resource_group,resource_execution_modes)
    for key,value in org_model.items():
        resource_group=string_to_list(key)
        new_value=[]
        for execution_mode in value:
            # 组相对比例
            grs=group_relative_stake(dataset,resources,resource_group,execution_mode,execution_mode_group)
            # 组覆盖范围
            gc=group_coverage(dataset, resources, resource_group, execution_mode, execution_mode_group)
            k1=float(k1)
            k2=float(k2)
            if k1*grs+(1-k1)*gc>=k2:
                new_value.append(execution_mode)
        org_model[key]=new_value.copy()
    return org_model



# 组相对比例
def group_relative_stake(dataset=[],resources=[],resource_group=[],execution_mode='',execution_mode_group=[]):
    resource_sum=len(dataset)
    rg_sum=0
    all_sum=0
    execution_mode_location=-1
    for eml in range(len(execution_mode_group)):
        if execution_mode==execution_mode_group[eml]:
            execution_mode_location=eml
            break
    resources_location = []
    for resource in resource_group:
        for i in range(len(resources)):
            if resource==resources[i]:
                resources_location.append(i)
    for i in range(resource_sum):
        if execution_mode_location==-1:
            raise Exception("An exception occurred in the fetch execution mode column")
        if i in resources_location and dataset[i][execution_mode_location]>0:
            rg_sum+=dataset[i][execution_mode_location]
        all_sum+=dataset[i][execution_mode_location]
    res=round(rg_sum/all_sum,3)
    return res

# 组覆盖范围
def group_coverage(dataset=[],resources=[],resource_group=[],execution_mode='',execution_mode_group=[]):
    execution_mode_location=-1
    resource_group_num=len(resource_group)
    size=0
    for eml in range(len(execution_mode_group)):
        if execution_mode==execution_mode_group[eml]:
            execution_mode_location=eml
            break
    resources_location = []
    for resource in resource_group:
        for i in range(len(resources)):
            if resource == resources[i]:
                resources_location.append(i)
    for rl in resources_location:
        if dataset[rl][execution_mode_location]>0:
            size+=1
    gc=size/resource_group_num
    return gc

# 用字典存储资源对应的执行模式(没有对应的执行模式次数)
def _resource_execution_modes(execution_mode_group=[],resources=[],dataset=[]):
    l=len(dataset)
    resource_execution_mode_dic={}
    for i in range(l):
        executions=[]
        for j in range(len(dataset[i])):
            if dataset[i][j]>0:
                executions.append(execution_mode_group[j])
        resource_execution_mode_dic[resources[i]]=executions
    return resource_execution_mode_dic

# 将字符串转化为数组
def string_to_list(str):
    str = str.lstrip()[1:len(str) - 1]
    list = str.split(',')
    for i in range(len(list)):
        s = list[i].strip()
        list[i] = s[1:len(s) - 1]
    return list