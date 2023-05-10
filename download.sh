#!/bin/bash -e

ARCHIVE=$1-1-1.dem.gz
DEMO=$1-1-1.dem
NAME=$1
wget -N --server-response https://storage.googleapis.com/demos-us-central1.faceit-cdn.net/csgo/$ARCHIVE 2>&1 >/dev/null | grep "HTTP/1.1 200\|HTTP/1.1 304" 
echo "File downloaded"
gzip -f -d $ARCHIVE
../cs-word-cloud -delimiter ', ' -input $DEMO > ${NAME}_words.txt
../weapon -delimiter ', ' -input $DEMO > ${NAME}_weapons.txt