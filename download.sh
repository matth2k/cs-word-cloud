#!/bin/bash

ARCHIVE=1-$1-1-1.dem.gz
DEMO=1-$1-1-1.dem
NAME=$1
wget https://storage.googleapis.com/demos-us-central1.faceit-cdn.net/csgo/$ARCHIVE
gzip -f -d $ARCHIVE
../cs-word-cloud -delimiter ', ' -input $DEMO > ${NAME}_words.txt
../weapon -delimiter ', ' -input $DEMO > ${NAME}_weapons.txt