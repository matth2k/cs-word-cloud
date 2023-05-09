package main

import (
	"flag"
	"fmt"
	"log"
	"os"

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

	tagSet := map[string]bool{}

	// Register handler on kill events
	p.RegisterEventHandler(func(e events.ItemPickup) {
		weaponEnt := e.Weapon.Entity
		if weaponEnt == nil {
			return
		}
		weaponProp := weaponEnt.Property("m_AttributeManager.m_Item.m_szCustomName")
		if weaponProp == nil || len(weaponProp.Value().StringVal) < 2 {
			return
		}
		nameTag := weaponProp.Value().StringVal
		if !tagSet[nameTag] {
			fmt.Printf("%s%s", weaponProp.Value().StringVal, *delimiter)
			tagSet[nameTag] = true
		}
	})

	// Parse to end
	err = p.ParseToEnd()
	if err != nil {
		log.Panic("failed to parse demo: ", err)
	}
}
