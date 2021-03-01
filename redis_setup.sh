#!/bin/bash

#update
sudo apt update

#install redis
sudo apt install redis-server

#start redis-server
redis-server

#make sure redis is working
redis-cli ping