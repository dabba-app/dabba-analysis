from copy import deepcopy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

def kmeans(data):

    # Importing the dataset
    #data = pd.read_csv('xclara.csv')
    print("Input Data and Shape")
    #print(data.shape)
    print data

    # Getting the values and plotting it
    f1 = np.array(data['V1'])*1000000
    f2 = np.array(data['V2'])*1000000
    X = np.array(list(zip(f1, f2)))

    #plt.scatter(f1, f2, c='black', s=7)

    # Euclidean Distance Caculator
    def dist(a, b, ax=1):
        return np.linalg.norm(a - b, axis=ax)

    # Number of clusters = no of dustbins / 50; max clusters = number of trucks
    k = int(np.ceil(len(X) / 10.0))

    print(k)
    # X coordinates of random centroids
    C_x = np.random.randint(np.min(X[:,0]), np.max(X[:,0]), size=k)
    # Y coordinates of random centroids
    C_y = np.random.randint(np.min(X[:,1]), np.max(X[:,1]), size=k)

    C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
    print("Initial Centroids")
    print(C)

    # Plotting along with the Centroids
    # plt.scatter(f1, f2, c='#050505', s=7)
    # plt.scatter(C_x, C_y, marker='*', s=200, c='g')


    # To store the value of centroids when it updates
    C_old = np.zeros(C.shape)
    # Cluster Lables(0, 1, 2)
    clusters = np.zeros(len(X))
    print(C.shape)
    print(len(X))
    print(X.__class__)
    print(X.shape)
    # Error func. - Distance between new centroids and old centroids
    error = dist(C, C_old, None)
    # Loop will run till the error becomes zero
    while error != 0:
        # Assigning each value to its closest cluster
        for i in range(len(X)):
            distances = dist(X[i], C)
            #returns index of the min element
            cluster = np.argmin(distances)
            clusters[i] = cluster
        # Storing the old centroid values
        C_old = deepcopy(C)
        # Finding the new centroids by taking the average value
        for i in range(k):
            points = [X[j] for j in range(len(X)) if clusters[j] == i]
            if len(points) != 0:
                C[i] = np.mean(points, axis=0)
        error = dist(C, C_old, None)

    X = X / 1000000;
    C = C / 1000000;
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    fig, ax = plt.subplots()
    for i in range(k):
            points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
            #print(points)
            if len(points) != 0:
                ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
    ax.scatter(C[:, 0], C[:, 1], marker='*', s=200, c='#050505')
    plt.show()
    return clusters, C, X