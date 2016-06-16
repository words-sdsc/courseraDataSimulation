#!/bin/sh

# get anaconda
wget http://repo.continuum.io/archive/Anaconda3-4.0.0-Linux-x86_64.sh

# install anaconda
bash Anaconda3-4.0.0-Linux-x86_64.sh


sudo yum install -y python-pip
sudo pip install --upgrade pip

sudo pip uninstall -y numpy

sudo pip uninstall -y pandas

sudo pip install -U --force nose

sudo pip install numpy

sudo pip install pandas