#!/bin/bash

# USAGE: ./productionize.sh <.pem file> <EC2 ip address>

# inputs IP, pem file location
if [ $# -ne 2 ]; then
    echo 'Please enter your pem location and EC2 public DNS as ./copy_to_prod.sh pem-full-file-location EC2-Public-IPv4-DNS'
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

# send prod host dependency installation script to EC2
scp -i $1 ./deploy_helpers/install_deps.sh ubuntu@$2:~/.

# ssh into the EC2, install prod dependencies (mostly docker), & start containerized app
ssh -t -i $1 ubuntu@$2 "unzip -o stonk-monitor.zip; chmod +x install_deps.sh; ./install_deps.sh; cd stonk-monitor; make up"
