#!/usr/bin/env bash

sudo apt-get update
# Install build-essential stuff
sudo apt-get install -y build-essential git diffstat gawk chrpath \
    texinfo libtool gcc-multilib dfu-util vim 

# Install latest version of node.js
sudo apt-get update
sudo apt-get install -y python-software-properties python g++ make
sudo add-apt-repository -y ppa:chris-lea/node.js
sudo apt-get update
sudo apt-get install -y nodejs

# Install bluetooth dev header files
sudo apt-get install -y libbluetooth-dev

# Install global NPM packages for development
sudo npm install -g cylon-ble

# Fix npm permissions
sudo chown -R vagrant "/usr/lib/node_modules/"