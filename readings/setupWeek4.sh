#!/bin/sh

sudo yum install -y python-pip

pip uninstall numpy

pip uninstall pandas

pip install numpy --user

pip install pandas --user