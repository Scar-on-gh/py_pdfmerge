#!/bin/bash
# ----------------------------------------------------
# Title:      setup_venv.sh
# License:    agpl-3.0
# Author:     Samuel Carlson (sa.d.carlson@gmail.com)
# Created on: 2022-12-19
# Editor:     
# Edited on:  
# ----------------------------------------------------
#
# Description: The purpose of this script is to setup the venv for pdfmerge.py tool.
# 
# Arguments:  None
# ----------------------------------------------------
#
# Notes:  
#
# TODO:         None at this time.
# ----------------------------------------------------

# ----------------------------------------------------
# Function    : main()
# Description : Does main-y things.
# ----------------------------------------------------
main(){
  pip3 install virtualenv
  virtualenv -p python3.11 ./venv/py3.11
  pip3 install -r requirements.txt
} # end main()

# To start the script we call main.
main $@;