#!/bin/bash

file_uri=$1
file_path=$2

if [ -e ${file_path} ]
then
    echo "Skip download step. ${file_path} already exists."
else
    echo "Downloading ${file_uri}"
    wget ${file_uri} -O ${file_path}
fi
