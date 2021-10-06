#!/bin/bash

# This is meant to be ran on the prod host system
# A system dependency installation script that mostly installs Docker

# ref: https://docs.docker.com/engine/install/ubuntu/

echo "Starting production system dependency install..."

# Uninstall old versions
sudo apt-get remove docker docker-engine docker.io containerd runc

# Update apt-get
sudo apt-get update

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --yes --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get -y install \
  apt-transport-https \
  ca-certificates \
  gnupg \
  lsb-release \
  make \
  unzip

# 2nd apt-get update

# Install Docker Engine
sudo apt-get -y install docker-ce docker-ce-cli containerd.io

# Install docker compose
sudo curl -sL "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

echo ""
echo "SUCCESSFULLY INSTALLED PRODUCTION DEPENDENCIES"
echo ""
