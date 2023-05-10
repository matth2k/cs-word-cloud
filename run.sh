#!/bin/bash
cd demos
cat ../matches.txt | xargs -t -n1 ../download.sh
cd ..
rm -f words.txt
find demos -maxdepth 2 -type f -name "*_words.txt" | xargs -t -n1 cat >> words.txt
wordcloud_cli --width 2000 --height 4000 --no_collocations --background white --stopwords blacklist.txt --text words.txt --imagefile wordcloud.png