def cross_validation_score(
        X, # 资源文件 profiles
        miner, # 组织模型挖掘器 _ahc(profiles, n_groups, method='single', metric='euclidean')
        miner_params, # 组织模型挖掘器参数
        proximity_metric='euclidean', # 欧几里得距离
        cv_fold=0.2 # 20%用于测试，80%用于训练
    ):
    """This method implements the cross validation method for
    determining an appropriate number of clusters for those
    organizational model miners employing clustering-liked algorithms.

    Parameters
    ----------
    X : DataFrame
        Resource profiles as input to an organizational model miner.
    miner : function
        An organizational model miner.
    miner_params : dict
        Other keyword parameters for the specified miner.
    proximity_metric : str, optional, default 'euclidean'
        Metric for measuring the distance while calculating proximity.
        This should remain consistent with that employed by the specific
        mining method. Defaults to ``'euclidean'``, meaning that
        euclidean distance is used for measuring proximity.
    cv_fold : int, or float in range (0, 1.0), default 0.2
        The number of folds to be used for cross validation.
        If an integer is given, then it is used as the fold number;
        if a float is given, then a corresponding percentage of data
        will be used as the test fold. Defaults to ``0.2``, meaning that
        20% of data will be used for testing while the other 80% used for
        training.

    Returns
    -------
    float
        The validation score as a result.

    Notes
    -----
    Refer to scipy.spatial.distance.pdist for more detailed explanation
    of proximity metrics.
    """
    scores = list()

    # split input dataset into specific number of folds 分割输入数据集到特定数量的折叠
    from copy import copy
    index = copy(list(X.index))
    from numpy import array_split
    if type(cv_fold) is float and 0 < cv_fold and cv_fold < 1.0:
        cv_fold = int(1.0 / cv_fold)  # 分成cv_fold份
    index_folds = array_split(index, cv_fold) # 将数据集分成cv_fold份
    print('Using cross validation with {} folds:'.format(cv_fold))
    from numpy import array, amin, mean
    from scipy.spatial.distance import cdist
    # 遍历
    for i in range(cv_fold):
        # split test set and train set
        test_set_index = index_folds[i] # 将第i份数据作为测试集
        train_set_index = list() # 将其他数组作为训练集
        for j in range(cv_fold):
            if j != i:
                train_set_index.extend(index_folds[j])

        # find the clusters using the train set
        result = miner(X.loc[train_set_index], **miner_params) # 使用挖掘方法获取训练集结果
        clusters = result[0] if type(result) is tuple else result # 聚类

        # calculate the cluster centroid 计算聚类质心
        # NOTE: different definitions of centroids may be used
        # 计算各个聚类中心
        cluster_centroids = list()
        for c in clusters:
            cluster_centroids.append(mean([X.loc[ix] for ix in c], axis=0))
        cluster_centroids = array(cluster_centroids)

        # evaluate using the test set 通过测试集验证
        sum_closest_proximity = 0.0
        for ix in test_set_index:
            x = X.loc[ix].values.reshape((1, len(X.loc[ix])))
            sum_closest_proximity += amin(
                cdist(x, cluster_centroids, metric=proximity_metric))
        scores.append((-1) * sum_closest_proximity)
    return mean(scores)