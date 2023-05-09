#!/bin/bash
rm -f words.txt
find demos -maxdepth 2 -type f -name "*.dem" | xargs -t -n1 ./cs-word-cloud -delimiter ', ' -input >> words.txt
wordcloud_cli --width 2000 --height 4000 --no_collocations --background white --stopwords blacklist.txt --text words.txt --imagefile wordcloud.png