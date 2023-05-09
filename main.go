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
		fmt.Printf("failed to open demo file %s\n", *input)
		panic(err)
	}
	defer f.Close()

	p := dem.NewParser(f)
	defer p.Close()

	// Register handler on kill events
	p.RegisterEventHandler(func(e events.ChatMessage) {
		words := strings.Fields(e.Text)
		for _, word := range words {
			if len(word) > 3 {
				fmt.Printf("%s%s", word, *delimiter)
			}
		}
	})

	// Parse to end
	err = p.ParseToEnd()
	if err != nil {
		log.Panic("failed to parse demo: ", err)
	}
}
