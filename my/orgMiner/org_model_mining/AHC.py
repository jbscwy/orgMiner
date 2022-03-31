# 凝聚层次聚类
'''
思路：
1.将每个数据都表示为一个簇
2.将两个最相似的簇合并成一个簇
3.重复步骤2，直到达到指定簇的数量
'''
from collections import OrderedDict
from copy import copy
from operator import itemgetter

from numpy import mean

# AHC

from my.orgMiner.org_model_mining.assign_execution_modes import _resource_execution_modes, overall_score
from my.orgMiner.org_model_mining.model_evalute import resource_functional_Similarity, _precision, _fitness
from my.orgMiner.org_model_mining.resource_classification import *


def agglomerative_hierarchical_clustering(dataset, resources, k, distance_method_option='0'):
    distance_method_option=str(distance_method_option)
    l = len(dataset)
    # 将每个点归为一个簇
    groups = []
    for i in range(len(resources)):
        group = []
        group.append(resources[i])
        groups.append(group)
    # print("初始簇："+str(groups))
    # 计算每个资源特征向量之间的距离
    disP2P = {}
    simP2P = {}
    distance = 0
    similar = 0
    for i in range(l):
        for j in range(l):
            if i < j:
                if distance_method_option == '0':
                    distance = Euclidean_distance(dataset[i], dataset[j])
                    disP2P[str(resources[i]) + "_to_" + resources[j]] = distance
                    continue
                if distance_method_option == '1':
                    distance = hammingDistance(dataset[i], dataset[j])
                    disP2P[str(resources[i]) + "_to_" + resources[j]] = distance
                    continue
                if distance_method_option == '2':
                    similar = pearson_r(dataset[i], dataset[j])
                    simP2P[str(resources[i]) + "_to_" + resources[j]] = similar
                    continue
                if distance_method_option == '3':
                    distance = spatial_difference(dataset[i], dataset[j])
                    disP2P[str(resources[i]) + "_to_" + resources[j]] = distance
                    continue
                if distance_method_option == '4':
                    similar = cosine(dataset[i], dataset[j])
                    simP2P[str(resources[i]) + "_to_" + resources[j]] = similar
                    continue
    if distance_method_option=='0' or  distance_method_option=='1' or  distance_method_option=='3':
        # 按距离降序将各个点对排序
        disP2P = OrderedDict(sorted(disP2P.items(), key=itemgetter(1), reverse=True))
    else:
        # 按相似度升序排序
        simP2P = OrderedDict(sorted(simP2P.items(), key=itemgetter(1), reverse=False))
    # # 当前簇的个数
    groupNum = len(groups)
    # 聚类到指定组数
    finalGroupNum = int(k)
    # 如果大于指定组数
    while groupNum > finalGroupNum:
        # 选取下一个距离最近的点对
        if distance_method_option in ['0', '1', '3']:
            twopoins, distance = disP2P.popitem()
        else:
            twopoins, distance = simP2P.popitem()
        pointA = twopoins.split('_to_')[0]
        pointB = twopoins.split('_to_')[1]
        pointA_location = get_location(pointA, groups)
        pointB_location = get_location(pointB, groups)
        pointAGroup = groups[pointA_location]
        pointBGroup = groups[pointB_location]

        # 若当前距离最近的两个点不在同一簇中，将B中所有点合并到A中，簇数减1
        if pointAGroup != pointBGroup:
            merge_array(groups, pointA_location, pointB_location)
            # print(groups)
            groupNum -= 1
    return groups


# 合并二维数组中指定两个数组
def merge_array(groups, i, j):
    groups[i].extend(groups[j])
    groups.pop(j)


# 判断某资源在资源组中的位置
def get_location(resource, groups=[]):
    for i in range(len(groups)):
        if resource in groups[i]:
            return i
    return -1


# 指定一个k进行交叉验证
def one_k_cross_validation(dataset_array, resources=[], k='', distance_method_option='1', cv_num=5):
    '''
    步骤：
    1.将全部资源平分成5等份或其他等份，将其中一份当成测试集，其余当成训练集
    2.遍历输入的资源组分组K的范围，使用凝聚层次算法对训练集进行聚类分组
    3.将每组中资源特征向量的矩阵的平均值作为聚类矩心
    4.遍历测试集中的资源组，获取资源对应的特征向量，计算该特征向量到聚类矩心的最小距离
    5.获取测试集资源组中每个资源特征向量到聚类矩心的最小距离总和，所得值的倒数就是一次交叉验证的分数
    6.交叉验证5次，取平均值，该值就是将资源分成K组的分数
    7.取分数最大值对应的K就是最佳分组
    :return:
    '''
    scores = list()
    index = copy(resources)
    size = int(cv_num)
    from numpy import array_split
    index_folds = array_split(index, size)  # 将资源{size}分组
    print('Using cross validation with {} folds:'.format(size))

    for i in range(size):
        test_set_index = index_folds[i]  # 测试集
        train_set_index = list()  # 训练集
        for j in range(size):
            if j != i:
                train_set_index.extend(index_folds[j])
        # find the clusters using the train set
        clusters =  agglomerative_hierarchical_clustering(dataset_array, resources, k, distance_method_option)
        # calculate the cluster centriod
        # NOTE: different definitions of centroids may be used
        cluster_centroids = list()
        for c in clusters:
            # computer the mean of the eigenvectors of all resources in the resource group
            cluster_centroids.append(resource_group_mean(dataset_array, resources, c))
        # evaluate using the test set

        # get the array of the test resource vector
        test_resource_array = []
        for i in range(len(resources)):
            for tc in test_set_index:
                if tc == resources[i]:
                    test_resource_array.append(dataset_array[i])
        score = test_score(cluster_centroids, test_resource_array)
        scores.append(score)
    return mean(scores)


# 交叉验证，返回最适合的k值
def cross_validation(dataset_array, resources=[], ks=[], distance_method='1', cv_num=5):
    max = -float('inf')
    best_k = ks[0]
    for k in ks:
        score = one_k_cross_validation(dataset_array, resources, k,
                                       distance_method, cv_num)
        print(str(k)+"_score:"+str(score))
        if score > max:
            max = score
            best_k = k
    return best_k


# 计算每个资源组对应的特征向量的平均值
def resource_group_mean(dataset_array=[], all_resources=[], resource_group=[]):
    size = len(dataset_array[0])
    resouce_len = len(all_resources)
    mean_array = []
    for i in range(size):
        sum = 0
        for resource in resource_group:
            for j in range(len(all_resources)):
                if resource == all_resources[j]:
                    sum += float(dataset_array[j][i])
        mean_array.append(copy(sum) / resouce_len)
    return mean_array


# 使用测试集评估
def test_score(cluster_centroids=[], test_resource_array=[]):
    sum = 0
    for test_resource in test_resource_array:
        min = float('inf')
        for cluster_centroid in cluster_centroids:
            distance = Euclidean_distance(test_resource, cluster_centroid)
            if distance < min:
                min = distance
        sum += min
    return 1 / sum

if __name__ == '__main__':
    file='re_test.csv'
    # Resource group
    dataset = make_execution__mode(file)
    resource_group, execution_mode_group = get_resource_group_and_execution_mode_group(file)
    dataset_array = reource_feature_matrix(dataset, resource_group, execution_mode_group)
    # get resource feature array
    resource_similarity_method_option='1'
    num_groups=[4,5]
    distance_method = '1'
    best_k = cross_validation(dataset_array, resource_group, num_groups,'1', 5)
    print(best_k)
    after_resource_group =  agglomerative_hierarchical_clustering(dataset_array, resource_group, best_k,
                                                             resource_similarity_method_option)
    rem = _resource_execution_modes(execution_mode_group, resource_group, dataset_array)
    # org_model = _fullRecall(after_resource_group, rem)
    org_model = overall_score(dataset_array, resource_group, execution_mode_group,
                                                     after_resource_group, rem, 0.8,
                                                     0.8)

    print(org_model)
    fit=_fitness(dataset, org_model)
    pre=_precision(dataset,org_model)
    print("resources number:"+str(len(resource_group)))
    print("execution_modes number:"+str(len(execution_mode_group)))
    print("fitness:" + str(fit))
    print("precision:" + str(pre))

    rfs = resource_functional_Similarity(dataset, org_model)
    print("resource functional similarity:" + str(rfs))

    fit_pre = float(float(fit) + float(pre) + float(rfs)) / 3
    print("fit_pre:"+str(fit_pre))

