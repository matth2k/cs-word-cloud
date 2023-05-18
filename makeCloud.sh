#!/bin/bash
cd demos
cat ../matches.txt | xargs -t -n1 ../download.sh
cd ..
rm -f words.txt
find demos -maxdepth 2 -type f -name "*_words.txt" | xargs -t -n1 cat >> words.txt
python3 csgoman.py
