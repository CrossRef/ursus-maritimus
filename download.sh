#!/bin/bash
datestamp=$(date +%y-%m-%d-%H:%M:%S)
dirname="run/$datestamp"
mkdir -p $dirname
cp urls.txt $dirname/urls.txt
cd $dirname
echo "Downloading into $dirname"
wget --verbose --header="CR-TDM-Client-Token: $TDM_TOKEN" -i urls.txt