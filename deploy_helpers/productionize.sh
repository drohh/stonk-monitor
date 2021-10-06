#!/bin/bash

# USAGE: ./productionize.sh <.pem file> <EC2 public IP address>

# exit if not enough arguments
if [ $# -ne 2 ]; then
    echo 'Please enter your pem location and EC2 public DNS as ./productionize.sh <path to .pem file> <EC2 public IP address>'
    exit 0
fi

# check if running from correct dir
if [[ "$PWD" != *stonk-monitor ]]; then
    echo "Please run this script from the project's base directory (stonk-monitor/)"
    exit 0
fi

# zip repo & leave it one directory up (..)
cd ..
rm -f stonk-monitor.zip
zip -r stonk-monitor.zip stonk-monitor/*
cd stonk-monitor

# send zipped repo to EC2
chmod 400 $1
scp -i $1 ../stonk-monitor.zip ubuntu@$2:~/.

# send scripts for dependency install and starting app
scp -i $1 ./deploy_helpers/install_deps.sh ./deploy_helpers/start_containerized_app.sh ubuntu@$2:~/.

# install prod system dependencies (mostly docker), and start app"
ssh -i $1 ubuntu@$2 "chmod +x install_deps.sh start_containerized_app.sh; ./install_deps.sh && ./start_containerized_app.sh"

