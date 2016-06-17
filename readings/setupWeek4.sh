#!/bin/sh

#Run this script ONCE on Cloudera VM
#This script prepares Cloudera VM for sparkMLlibCustering.py

#update Spark
sudo yum install -y spark-core spark-master spark-worker spark-history-server spark-python

#get Anaconda  
wget http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh

#install Anaconda
bash Anaconda3-4.0.0-Linux-x86_64.sh

# _________when you see --More-- keep pressing SPACE BAR
# _________answer yes to all questions