#!/bin/bash

# SETUP FILE FOR MACHINE LEARNING COURSE
 
# upgrade spark python to work with python 3
sudo yum upgrade -y spark-python

# update spark log4j to be quiet and restart
sudo service spark-master restart
sudo service spark-worker restart

# download and install anaconda for pandas, jupyter
wget http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh
bash Anaconda3-4.0.0-Linux-x86_64.sh

# set environment variables to load spark libs in jupyter
echo "export PYSPARK_DRIVER_PYTHON_OPTS=\"notebook\"" >> ~/.bashrc
echo "export PYSPARK_DRIVER_PYTHON=jupyter"  >> ~/.bashrc

source ~/.bashrc

# run 'pyspark' to start Spark and open Notebook
