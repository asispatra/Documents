#!/bin/bash

CURRENT_DIR=$PWD
mkdir -p ~/bin/
cd ~/bin/

wget "https://raw.githubusercontent.com/asispatra/Documents/master/scripts/create" -O create
wget "https://raw.githubusercontent.com/asispatra/Documents/master/scripts/cdm2c" -O cdm2c

chmod u+x *
cd ${CURRENT_DIR}
