package main

import (
	"fmt"
	"iter"
	"os"
	"os/signal"
	"strconv"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

func main() {
	go func() {
		c := make(chan os.Signal, 1)
		signal.Notify(c, os.Interrupt)
		<-c
		os.Exit(1)
	}()

	osStdout := os.Stdout
	os.Stdout = os.Stderr
	for result := range process(func(yield func(Task) bool) {
		for i := 1; i < len(os.Args); i += 3 {
			year, err := strconv.ParseUint(os.Args[i], 10, 16)
			check(err)
			day, err := strconv.ParseUint(os.Args[i+1], 10, 8)
			check(err)
			if !yield(Task{
				Year: uint16(year),
				Day:  uint8(day),
				Path: os.Args[i+2],
			}) {
				return
			}
		}
	}) {
		fmt.Fprintf(osStdout, "%s\n", result.Serialize())
	}
}

type Task struct {
	Year uint16
	Day  uint8
	Path string
}

func process(tasks iter.Seq[Task]) iter.Seq[aoc.Result] {
	return func(yield func(aoc.Result) bool) {
		for task := range tasks {
			days, ok := Years[task.Year]
			if !ok {
				if !yield(aoc.StrError("not implemented")) {
					return
				}
				continue
			}
			solver, ok := days[task.Day]
			if !ok {
				if !yield(aoc.StrError("not implemented")) {
					return
				}
				continue
			}
			if !yield(func() aoc.Result {
				f, err := os.Open(task.Path)
				if err != nil {
					return aoc.Error(err)
				}
				return solver(f)
			}()) {
				return
			}
		}
	}
}

func check(err error) {
	if err != nil {
		panic(err)
	}
}
