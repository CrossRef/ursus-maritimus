#!/bin/bash
datestamp=$(date +%y-%m-%d-%H:%M:%S)
outputdir="`pwd`/run/$datestamp"
latestdir="`pwd`/latest"
mkdir -p $outputdir
rm $latestdir
ln -s $outputdir $latestdir
cp urls.txt $outputdir/urls.txt
cd $outputdir
echo "Downloading into $outputdir"
wget --verbose --header="CR-TDM-Client-Token: $TDM_TOKEN" --header="CR-Clickthrough-Client-Token: $TDM_TOKEN" -i urls.txt

