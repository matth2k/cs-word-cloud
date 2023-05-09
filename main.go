package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	dem "github.com/markus-wa/demoinfocs-golang/v3/pkg/demoinfocs"
	events "github.com/markus-wa/demoinfocs-golang/v3/pkg/demoinfocs/events"
)

var (
	input     = flag.String("input", "f", "input demo")
	delimiter = flag.String("delimiter", "\n", "delimiter to use between fields")
)

func main() {

	flag.Parse()
	f, err := os.Open(*input)
	if err != nil {
		fmt.Fprintf(os.Stderr, "failed to open demo file %s\n", *input)
		panic(err)
	}
	defer f.Close()

	p := dem.NewParser(f)
	defer p.Close()

	// Register handler on kill events
	p.RegisterEventHandler(func(e events.ChatMessage) {
		words := strings.Fields(e.Text)
		for _, word := range words {
			wordSlice := strings.Trim(word, "/#,.!?;:()[]{}'-")
			finalWord := strings.ToLower(wordSlice)
			if len(finalWord) > 1 && len(finalWord) < 20 && !strings.Contains(finalWord, "the") && !strings.ContainsAny(finalWord, ",.!?;:()[]{}'") {
				fmt.Printf("%s%s", finalWord, *delimiter)
			}
		}
	})

	// Parse to end
	err = p.ParseToEnd()
	if err != nil {
		log.Panic("failed to parse demo: ", err)
	}
}
