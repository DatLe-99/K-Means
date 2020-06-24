import math, random
import matplotlib.pyplot as plt
from matplotlib import cm

class Kmeans:
    __centroids = dict()    #Dictionary of centroid and points belong to it with the form (centroid, list of points)
    __previousCentroids = list()    #List of the previous centroid
    __k = 2    #Number of cluster
    def __init__(self, listDataPoint):
        self.dataPoints = listDataPoint

    def getCentroids(self):
        return self.__centroids

    def EuclideDistance(self, pointA, pointB):
        return math.sqrt(pow(pointA[0]-pointB[0], 2)+ pow(pointA[1]-pointB[1], 2))

    def enoughDistance(self, point, listCurrentPoint):
        for p in listCurrentPoint:
            if(self.EuclideDistance(point, p) < self.minimumDis):
                return False
        return True

    def __chooseSampleCentroids(self, k):
        self.__centroids[random.choice(self.dataPoints)] = list()
        while(len(self.__centroids) < k ):
            tmp = random.choice(self.dataPoints)
            if(tmp not in self.__centroids and self.enoughDistance(tmp, self.__centroids.keys())):
                self.__centroids[tmp] = list()

    def __computeCentroid(self):
        self.__previousCentroids = self.__centroids.keys()
        newCentroids = dict()
        for cen, points in self.__centroids.items():
            sumX = 0
            sumY = 0
            for p in points:
                sumX += p[0]
                sumY += p[1]
            newCentroid = (round(sumX/len(points),2), round(sumY/len(points),2))
            newCentroids[newCentroid] = list()
        return newCentroids

    def __assignCluster(self):
        for p in self.dataPoints:
            listDistance = dict()
            for centroid in self.__centroids.keys():
                listDistance[centroid] = self.EuclideDistance(centroid, p)
            minCluster = min(listDistance, key=listDistance.get)
            self.__centroids[minCluster].append(p)

    def predict(self, k, enoughDistance):
        self.minimumDis = enoughDistance
        if(k <= 1):
            print("Number of cluster must be larger than 1\n")
            return
        self.__chooseSampleCentroids(k)
        curCentroid = self.__centroids
        while(self.__previousCentroids != curCentroid.keys()):
            self.__centroids = curCentroid
            self.__assignCluster()
            curCentroid = self.__computeCentroid()
        print(self.__centroids)

if __name__ == "__main__":
    f = open("points.txt", "r")
    datapoints = []
    for line in f:
        l = tuple(map(int, line.split()))
        datapoints.append(l)

    c = Kmeans(datapoints)
    c.predict(15, 150000)

    centroids = c.getCentroids()
    listCoordinates = []
    i = 0
    for centroid, points in centroids.items():
        i += 1
        for p in points:
            listCoordinates.append((p, i))

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    ax.set_title("Clustering", fontsize=14)
    ax.set_xlabel("X", fontsize=12)
    ax.set_ylabel("Y", fontsize=12)
    ax.grid(True, linestyle='-', color='0.75')

    x = [i[0][0] for i in listCoordinates]
    y = [i[0][1] for i in listCoordinates]
    cluster = [i[1] for i in listCoordinates]
    ax.scatter(x, y, s=40,c = cluster, marker='o', cmap=cm.jet)
    centroid_x = [i[0] for i in centroids]
    centroid_y = [i[1] for i in centroids]
    ax.scatter(centroid_x, centroid_y, s=60, marker='x', cmap=cm.jet)
    plt.show()





