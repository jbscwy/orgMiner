from my.orgMiner.org_model_mining import assign_execution_modes, resource_classification
from my.orgMiner.org_model_mining.AHC import cross_validation, agglomerative_hierarchical_clustering
from my.orgMiner.org_model_mining.k_means import kMeans
from my.orgMiner.org_model_mining.model_evalute import _fitness, resource_functional_Similarity, _precision


def org_model_mining_function(resource_log,organization_model_mining_method,similarity_method,k_range,assign_execution_method,w1,w2):
    # get resource log data
    resource_log_data = resource_classification.make_execution__mode(resource_log)
    # get resource groups and execution mode groups
    resource_group, execution_mode_group = resource_classification.get_resource_group_and_execution_mode_group(resource_log)
    # get resource feature array
    dataset_array = resource_classification.reource_feature_matrix(resource_log_data, resource_group, execution_mode_group)
    #
    # after_resource_group = []
    k_range = k_range[1:-1].split(',')
    k_range_list=[]
    k_range_list.append(k_range[0])
    k_range_list.append(k_range[1])
    # get best k
    best_k = cross_validation(dataset_array, resource_group, k_range_list,
                              '1', 5)
    if organization_model_mining_method == '0':
        # use K-Means
        after_resource_group = kMeans(dataset_array, resource_group, best_k,'1')
    elif organization_model_mining_method == '1':
        # use AHC
        after_resource_group = agglomerative_hierarchical_clustering(dataset_array, resource_group, best_k,
                                                         similarity_method)
    else:
        raise
    # get resource execution modes
    resource_execution_modes= assign_execution_modes._resource_execution_modes(execution_mode_group, resource_group, dataset_array)
    if assign_execution_method == 'full_recall':
        org_model = assign_execution_modes._fullRecall(after_resource_group, resource_execution_modes)
    # use overScore
    elif assign_execution_method == 'overall_score':
        org_model = assign_execution_modes.overall_score(dataset_array, resource_group, execution_mode_group,
                                                         after_resource_group, resource_execution_modes, w1, w2)
    else:
        raise

    # evaluate the organizational model
    fitness = _fitness(resource_log_data, org_model)
    precision = _precision(resource_log_data, org_model)
    resource_functional_similarity = resource_functional_Similarity(resource_log_data, org_model)

    log_info={
        'org_model':org_model,
        'fitness':fitness,
        'precision':precision,
        'resource_functional_similarity':resource_functional_similarity
    }

    return log_info


