
APIKEY?=TODO
INITMATCH?=TODO
MATCH_COUNT=1000

all: word_cloud.png

word_cloud.png: words.txt
	python3 csgoman.py

words.txt: matches.txt cs-word-cloud
	mkdir -p demos
	./makeWords.sh

cs-word-cloud:
	go build

matches.txt:
	rm -f $@
	@echo "This will take a while..."
	python3 scrapeGames.py -s $(INITMATCH) -k $(APIKEY) -n $(MATCH_COUNT) | tee -a $@

clean:
	rm -rf matches.txt words.txt word_cloud.png demos cs-word-cloud