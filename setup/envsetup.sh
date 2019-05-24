#!/bin/bash


# Setting up aardvark and repokid environment
echo "Setting up environment folder for aardvark and repokid..."
wget https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.tar.gz

sudo apt install awscli -y || sudo yum install awscli -y
sudo apt install python2.7 -y || sudo yum install python2.7 -y
sudo apt install python2-pip -y || sudo yum install python2-pip -y


# initializing folder
echo "Creating separate directory..."
mkdir ../aardvark_repokid_demo
cd ../aardvark_repokid_demo
mkdir aardvark_repokid
mkdir dynamodb_local

# Providing local environment for dynamodb
echo "Unzipping local DynamoDB for environment testing..."
cd dynamodb_local
tar xzvf ../../setup/dynamodb_local_latest.tar.gz 

# Creating aardvark/repokid dir.
echo "Setting up Aardvark & Repokid"
cd ../aardvark_repokid

mkdir aardvark
echo "Cloning Aardvark github environment..."
cd aardvark
git clone git@github.com:Netflix-Skunkworks/aardvark.git
cd ..

# copying files
mkdir customize
cp "../../setup/custom_configs.json" "./customize/custom_repokid_configs.json"
cp "../../setup/base_configs.json" "./customize/default_repokid_configs.json"

mkdir repokid
echo "Cloning Repokid github environment..."
cd repokid
git clone git@github.com:Netflix/repokid.git
cd ../../

# Create a virtual environment Python-2.7 with environment requirements
echo "Ensure Python2.7/Virtual-Environmoent is installed... Attempting to create virtual environment with Python2.7..."

python2 -m pip install virtualenv
python2 -m virtualenv aardvark_repokid_env
