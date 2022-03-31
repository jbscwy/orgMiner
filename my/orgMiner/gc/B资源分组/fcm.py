global MAX  # 用于初始化隶属度矩阵U
MAX = 10000.0

global Epsilon  # 结束条件
Epsilon = 0.0000001


def _fcm(profiles,cluster_number,centers,m):
    """
    这是主函数，它将计算所需的聚类中心，并返回最终的归一化隶属矩阵U.
    输入参数：簇数(cluster_number)、隶属度的因子(m)的最佳取值范围为[1.5，2.5]
    """
    from 处理数据.get_data_resources_by_profile import get_data_resources_by_profile
    dataset_list,resource_group=get_data_resources_by_profile(profiles)

    # # 初始化隶属度矩阵U
    # U = initialize_U(data, cluster_number)
    # print_matrix(U)

    # print(centers)
    # 循环更新U
    n = 0
    while (True):
        # print("迭代次数：",n)
        n = n + 1
        # 创建它的副本，以检查结束条件
        import copy
        centers_old = copy.deepcopy(centers)
        # 计算隶属矩阵
        U = [[0 for col in range(cluster_number)] for row in range(len(dataset_list))]
        # 创建一个距离向量, 用于计算U矩阵。
        distance_matrix = []
        for i in range(0, len(dataset_list)):
            current = []
            for j in range(0, cluster_number):
                current.append(distance(dataset_list[i], centers[j]))
            distance_matrix.append(current)
        # 计算U
        for j in range(0, cluster_number):
            for i in range(0, len(dataset_list)):
                dummy = 0.0
                for k in range(0, cluster_number):
                    # 分母
                    if distance_matrix[i][k] == 0:
                        continue
                    dummy += (distance_matrix[i][j] / distance_matrix[i][k]) ** (2 / (m - 1))
                if dummy == 0.0:
                    U[i][j] = 0.0
                else:
                    U[i][j] = 1 / dummy

        # 更新聚类中心
        for j in range(0, cluster_number):
            current_cluster_center = []
            for i in range(0, len(dataset_list[0])):
                dummy_sum_num = 0.0
                dummy_sum_dum = 0.0
                for k in range(0, len(dataset_list)):
                    # 分子
                    dummy_sum_num += (U[k][j] ** m) * dataset_list[k][i]
                    # 分母
                    dummy_sum_dum += (U[k][j] ** m)
                # 第i列的聚类中心
                current_cluster_center.append(dummy_sum_num / dummy_sum_dum)
            # 第j簇的所有聚类中心
            centers[j] = current_cluster_center

        if end_conditon(centers, centers_old):
            # print("已完成聚类")
            break

    U = normalise_U(U)
    import numpy as np
    labels = np.argmax(U, axis=1)
    return labels


def distance(point, center):
    """
    该函数计算2点之间的距离（作为列表）。我们指欧几里德距离。闵可夫斯基距离
    """
    if len(point) != len(center):
        return -1
    dummy = 0.0
    for i in range(0, len(point)):
        dummy += abs(point[i] - center[i]) ** 2
    import math
    return math.sqrt(dummy)


def end_conditon(U, U_old):
    """
	结束条件。当U矩阵随着连续迭代停止变化时，触发结束
	"""
    global Epsilon
    for i in range(0, len(U)):
        for j in range(0, len(U[0])):
            if abs(U[i][j] - U_old[i][j]) > Epsilon:
                return False
    return True


def normalise_U(U):
    """
    在聚类结束时使U模糊化。每个样本的隶属度最大的为1，其余为0
    """
    for i in range(0, len(U)):
        maximum = max(U[i])
        for j in range(0, len(U[0])):
            if U[i][j] != maximum:
                U[i][j] = 0
            else:
                U[i][j] = 1
    return U