# What this script does: This script creates two clusters and prints the cluster centers to file: 

# Where is the output of this script: clusterCenters.txt

# [STEP 1] 
# Before you can run this script in the Virtual Machine, you need numpy and pandas
# Open Applications->SystemTools->Terminal and type the following command:
# $ . ./setupWeek4.sh and hit Enter
# [wait] answer yes to all questions
# [wait] when you see --More-- keep pressing space bar

# [STEP 2]
# Change the path to files ad-clicks.csv and buy-clicks.csv to that on your machine

# [STEP 3] To run this script, write following on terminal, and hit enter:
# PYSPARK_PYTHON=/home/cloudera/anaconda3/bin/python spark-submit sparkMLlibClustering.py

import pandas as pd
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
import sys

conf = (SparkConf()
         .setMaster("local")
         .setAppName("My app")
         .set("spark.executor.memory", "1g"))
sc 			= SparkContext(conf = conf)
sqlContext 	= SQLContext(sc)

#Read ad-clicks.csv file

adclicksDF = pd.read_csv('/Users/aloksingh/Downloads/capstone/second/courseraDataSimulation/ad-clicks.csv')
adclicksDF = adclicksDF.rename(columns=lambda x: x.strip()) #remove whitespaces from headers
adclicksDF['adCount'] = 1 #each row is a single click, hence add extra column and make it =1

#Read buy-clicks.csv file

buyClicksDF = pd.read_csv('/Users/aloksingh/Downloads/capstone/second/courseraDataSimulation/buy-clicks.csv')
buyClicksDF = buyClicksDF.rename(columns=lambda x: x.strip()) #remove whitespaces from headers

#Select user attributes for clustering

userPurchases = buyClicksDF[['userid','price']] #select only userid and price
useradClicks = adclicksDF[['userid','adCount']]

#Perform aggregation to get total ad-clicks per user

adsPerUser = useradClicks.groupby('userid').sum()
adsPerUser = adsPerUser.reset_index()

#Perform aggregation to get total revenue generated per user

revenuePerUser = userPurchases.groupby('userid').sum()
revenuePerUser = revenuePerUser.reset_index()
trainingDF = adsPerUser.merge(revenuePerUser, on='userid') #userid, adCount, price

#Remove userid before training and keep other two attributes

pDF = sqlContext.createDataFrame(trainingDF)
parsedData = pDF.rdd.map(lambda line: array([line[1], line[2]])) #adCount, price (i.e. revenue)

#Train KMeans model to create two clusters

clusters = KMeans.train(parsedData, 2, maxIterations=10, runs=10, initializationMode="random")

#redirect stdout
orig_stdout = sys.stdout
f = open('clusterCenters.txt', 'w')
sys.stdout = f

#Display the centers of two clusters
print(clusters.centers)
print("First number is the # of ad-clicks and second number is revenue per user")
print("Compare the 1st number of each cluster to see how differently users behave when it comes to clicking ads")
print("Compare the 2nd number of each cluster to see how differently users behave when it comes to buying stuff")

#Redirect back the stdout
sys.stdout = orig_stdout
f.close()