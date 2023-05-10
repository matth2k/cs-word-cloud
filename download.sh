#!/bin/bash

ARCHIVE=$1-1-1.dem.gz
DEMO=$1-1-1.dem
NAME=$1
cat ../cdns.txt | while read line 
do
  wget -N --server-response $line/csgo/$ARCHIVE 2>&1 >/dev/null | grep "HTTP/1.1 200\|HTTP/1.1 304"
  if [ $? -eq 0 ]; then
    echo "File downloaded"
    break
  fi
done

if [ -f "$ARCHIVE" ]; then
  echo "Demo downloaded"
else 
  echo "Skipping demo"
  exit 1
fi

gzip -f -d $ARCHIVE
../cs-word-cloud -delimiter ', ' -input $DEMO > ${NAME}_words.txt
../weapon -delimiter ', ' -input $DEMO > ${NAME}_weapons.txt