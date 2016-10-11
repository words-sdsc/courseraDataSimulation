
from pyspark.ml.clustering import KMeans as KM
from pyspark.mllib.linalg import DenseVector
from math import sqrt
from numpy import array

def computeCost(featuresAndPrediction, model):
    allClusterCenters = [DenseVector(c) for c in model.clusterCenters()]
    arrayCollection   = featuresAndPrediction.rdd.map(array)

    def error(point, predictedCluster):
        center = allClusterCenters[predictedCluster]
        z      = point - center
        return sqrt((z*z).sum())
    
    return arrayCollection.map(lambda row: error(row[0], row[1])).reduce(lambda x, y: x + y)


def elbow(elbowset, wssseList, k_values):
	for howManyClusters in k_values:
		print "Training for k = {} ".format(howManyClusters)
		kmeans      = KM(k=howManyClusters, seed = 1)
		model       = kmeans.fit(elbowset)
		transformed = model.transform(elbowset)
		featuresAndPrediction     = transformed.select("features", "prediction")

		W = computeCost(featuresAndPrediction, model)
		print "......................WSSSE = {} ".format(W)

		wssseList.append(W)
