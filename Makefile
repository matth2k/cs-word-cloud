
APIKEY?=TODO
INITMATCH?=TODO
MATCH_COUNT=1000

all: word_cloud.png

word_cloud.png: words.txt
	python3 csgoman.py

words.txt: matches.txt
	mkdir -p demos
	./makeWords.sh

matches.txt:
	rm -f $@
	@echo "This will take a while..."
	python3 scrapeGames.py -s $(INITMATCH) -k $(APIKEY) -n $(MATCH_COUNT) | tee -a $@

clean:
	rm -f matches.txt words.txt word_cloud.png demos