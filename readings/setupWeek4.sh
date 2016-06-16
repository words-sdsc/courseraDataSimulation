#!/bin/sh

sudo yum install -y python-pip
sudo pip install --upgrade pip

sudo pip uninstall -y numpy

sudo pip uninstall -y pandas

sudo pip install -U --force nose

sudo pip install numpy

sudo pip install pandas