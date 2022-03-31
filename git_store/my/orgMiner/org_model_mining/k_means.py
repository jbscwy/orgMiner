# This Python file uses the following encoding: utf-8


# 随机初始化k个质心
from my.orgMiner.org_model_mining.resource_classification import *


def randCent(dataSet,k):
    # data=np.array(dataSet)
    # 得到数据集样本的维度
    n=np.shape(dataSet)[1]
    centroids=np.mat(np.zeros((int(k),int(n))))
    for j in range(n):
        #得到该列数据的最小值，最大值
        minJ=np.min(dataSet[:,j])
        maxJ=np.max(dataSet[:,j])
        #得到该列数据的范围（最大值-最小值）
        rangeJ=float(maxJ-minJ)
        #k个质心向量的第j维数据值随机位于（最小值，最大值）内的某一值
        centroids[:,j]=minJ+rangeJ*np.random.rand(k,1)
    # 返回初始化得到的k个质心向量
    return centroids

# # k-Means算法
def kMeans(dataSet,resources,k,method='1'):
    # 将数组转化为矩阵
    dataSet=np.array(dataSet)
    # 获取数据集样本数
    m=np.shape(dataSet)[0]
    n=np.shape(dataSet)[1]
    # 初始化一个（m,n）全零矩阵
    clusterAssment=[[0]*2 for _ in range(m)]
    # 创建初始的k个质心向量
    centroids=randCent(dataSet,k)
    # 判断聚类结果是否发生变化
    clusterChanged=True
    while clusterChanged:
        clusterChanged=False
        for i in range(m):
            minDist=np.inf #初始化最大值
            maxSimilar=0
            minIndex=-1
            for j in range(k):
                distJ=''
                simil=''
                if method=='1':
                    distJ=Euclidean_distance(centroids[j],dataSet[i])
                if method=='2':
                    distJ=hammingDistance(centroids[j],dataSet[i])
                if method=='3':
                    simil=pearson_r(centroids[j],dataSet[i])
                if method=='4':
                    distJ=spatial_difference(centroids[j],dataSet[i])
                if method=='5':
                    simil=cosine(centroids[j],dataSet[i])
                if method in ['1','2','4'] and distJ<minDist:
                    minDist=distJ #更新最小距离
                    minIndex=j
                if simil!='' and simil>maxSimilar:
                    maxSimilar=simil
                    minIndex=j
            if str(clusterAssment[i][0])!=str(minIndex): #如果中心点不变化，终止循环
                clusterChanged=True
            clusterAssment[i][0]=minIndex
            if method in ['1','2','4']:
                clusterAssment[i][1]=minDist # 将index，k值中心点和最小距离存入到数组中
            if method in ['3','5']:
                clusterAssment[i][1]=maxSimilar
        print(centroids)

        # 更换中心点的位置
        for cent in range(k):
            # 通过数据过滤获得给定的所有点
            ptsInClust=[]
            for i in range(len(clusterAssment)):
                if clusterAssment[i][0]==cent:
                    ptsInClust.append(dataSet[clusterAssment[i][0]])
            if len(ptsInClust)==0:
                continue
            # 得到更新后的中心点
            data=ptsInClust.copy()
            centroids[cent,:]=arrays_average(data)

        # for cent in range(k):
        #     ptsInClust=dataSet[np.nonzero(clusterAssment[cent][0])]
        #     centroids[cent]=np.mean(ptsInClust,axis=0) #得到更新后的中心点
    dic={}
    l=len(clusterAssment)
    for i in range(l):
        if clusterAssment[i][0] in dic.keys():
            value=dic[clusterAssment[i][0]]
            value.append(i)
        else:
            value=[]
            value.append(i)
            dic[clusterAssment[i][0]]=value
    resource_group=[]
    for value in dic.values():
        rg=[]
        for i in range(len(value)):
            rg.append(resources[value[i]])
        resource_group.append(rg.copy())
    return centroids,clusterAssment,resource_group



# 取多个数组的平均值
def arrays_average(data):
    res=[]
    row=len(data)
    col=len(data[0])
    for j in range(col):
        sum=0
        for i in range(row):
            sum+=data[i][j]
        res.append(sum/row)
    return res


def initCentroids(data, k):
    k=int(k)
    numSamples, dim = data.shape
    # k个质心，列数跟样本的列数一样
    # if numSamples<k:
    #     k=numSamples

    centroids = np.zeros((k, dim))
    # 随机选出k个质心
    for i in range(k):
        # 随机选取一个样本的索引
        index = int(np.random.uniform(0, numSamples))
        # 作为初始化的质心
        centroids[i, :] = data[index, :]
    return centroids


def kmeans0(dataset, k,method='1'):
    '''
    创建K个质心,然后将每个店分配到最近的质心,再重新计算质心。
    这个过程重复数次,直到数据点的簇分配结果不再改变为止
    :param dataMat: 数据集
    :param k: 簇的数目
    :param distMeans: 计算距离
    :param createCent: 创建初始质心
    :return:
    '''
    # 样本的个数
    dataset=np.array(dataset)
    m = np.shape(dataset)[0]
    # 保存每个样本的聚类情况，第一列表示该样本属于某一类，第二列是与聚类中心的距离
    clusterAssment = np.mat(np.zeros((m, 2)))
    # 产生随机质心,将列表形式转换为数组形式
    centroids = np.array(initCentroids(dataset, k))
    # 控制聚类算法迭代停止的标志，当聚类不再改变时，就停止迭代
    clusterChanged = True
    while clusterChanged:
        # 先进行本次迭代，如果聚类还是改变，最后把该标志改为True，从而继续下一次迭代
        clusterChanged = False
        for i in range(m):  # 遍历每一个样本
            # 每个样本与每个质心计算距离
            # 采用一趟冒泡排序找出最小的距离，并找出对应的类
            # 计算与质心的距离时，刚开始需要比较，记为无穷大
            mindist = np.inf
            distj=np.inf
            minj=-1
            for j in range(k):  # 遍历每一类
                #                 print(np.array(dataset[i,:]))
                #                 print(centroids)
                if method == '1':
                    distj = Euclidean_distance(centroids[j, :], dataset[i, :])
                if method == '2':
                    distj = hammingDistance(centroids[j, :], dataset[i, :])
                if method == '4':
                    distj = spatial_difference(centroids[j, :], dataset[i, :])
                if method == '3':
                    distj = -pearson_r(centroids[j, :], dataset[i, :])
                if method == '5':
                    distj = -cosine(centroids[j, :], dataset[i, :])
                if distj < mindist:
                    mindist = distj
                    minj = j
            # 遍历完k个类，本次样本已聚类
            if clusterAssment[i, 0] != minj:  # 判断本次聚类结果和上一次是否一致
                clusterChanged = True  # 只要有一个聚类结果改变，就重新迭代
            clusterAssment[i, :] = minj, mindist ** 2  # 类别，与距离
        # 外层循环结束，每一个样本都有了聚类结果

        # 更新质心
        for cent in range(k):
            # 找出属于相同一类的样本
            data_cent = dataset[np.nonzero(clusterAssment[:, 0].A == cent)[0]]
            centroids[cent, :] = np.mean(data_cent, axis=0)
    return centroids, clusterAssment


# 使用K-means算法交叉验证
# 指定一个k进行交叉验证
def one_k_cross_validation_in_kmeans(dataset_array, resources, k, distance_method_option='1', cv_num=5):
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
    index = np.copy(resources)
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
        # clusters = coagulate_hierarchical_clustering(dataset_array, resources, k, distance_method_option)
        clusters = kMean(dataset_array, int(k),resources,distance_method_option)
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
    return np.mean(scores)


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

# 交叉验证，返回最适合的k值
def cross_validation_in_kmeans(dataset_array, resources=[], ks=[], distance_method='1', cv_num=5):
    max = 0
    best_k = ks[0]
    for k in ks:
        score = one_k_cross_validation_in_kmeans(dataset_array, resources, k,
                                       distance_method, cv_num)
        if score > max:
            max = score
            best_k = k
    return best_k

#获取资源组
def kMean(dataMat, k,resources,method='1'):
    groups={}
    centroids, clusterAssment=kmeans0(dataMat, k, method)
    clusterAssment=clusterAssment.A
    print('clusterAssment:'+str(len(clusterAssment)))
    for row in range(len(clusterAssment)):
        if clusterAssment[row][0] not in groups.keys():
            res=[]
            res.append(resources[row])
            groups[clusterAssment[row][0]]=res
        else:
            res=groups[clusterAssment[row][0]]
            res.append(resources[row])
            groups[clusterAssment[row][0]]=res
    resources=[]
    for value in groups.values():
        resources.append(value)
    return resources


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
        mean_array.append(np.copy(sum) / resouce_len)
    return mean_array




if __name__ == '__main__':
    N=[[2, 0, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0, 0],
                        [0, 0, 0, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 1, 1]]
    resources = ['Pete', 'Ann', 'John', 'Sue', 'Bob', 'Mary']

    centroids, clusterAssment=kmeans0(N,4,'1')
    print(centroids)
    print(clusterAssment)

    resources=kMean(N, 4, resources, '1')
    print(resources)





















