import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # 支持中文
    import matplotlib as mpl
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    K = range(2, 7)
    X=[[2,0,0,0,0,0,0,0,0,0,0],
       [0,1,0,0,1,0,0,0,0,0,0],
       [0,0,0,1,0,0,0,0,0,0,0],
       [0,0,1,1,0,0,0,0,0,0,0],
       [0,0,1,0,0,2,1,0,0,0,1],
       [0,0,0,0,0,0,0,1,1,1,0]]
    X=np.array(X)

    meanDispersions = []
    for k in K:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        #理解为计算某个与其所属类聚中心的欧式距离
        #最终是计算所有点与对应中心的距离的平方和的均值
        meanDispersions.append(sum(np.min(cdist(X, kmeans.cluster_centers_, 'euclidean'), axis=1)) / X.shape[0])

    plt.plot(K, meanDispersions, 'bx-')
    plt.xlabel('k')
    plt.ylabel('SSE')
    plt.title('用手肘法选择K值')
    plt.show()