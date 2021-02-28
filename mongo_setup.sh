#!/bin/bash

#Import the public key used by the package management system
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -

#Create a list file for MongoDB
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list

#Reload local package database
echo UPDATING
sudo apt-get update

#Install the MongoDB packages
echo INSTALLING MONGODB
sudo apt-get install -y mongodb-org

#Make sure MongoDB starts after system reboot
sudo systemctl enable mongod

#Get status of MongoDB
sudo systemctl status mongod

#Start MongoDB
sudo systemctl start mongod

#Get status of MongoDB
sudo systemctl status mongod


