package y2025

import (
	"bufio"
	"container/heap"
	"io"
	"slices"
	"strconv"
	"strings"

	"github.com/Grub4K/aoc-solutions/go/aoc"
)

type d08Vector3 struct {
	X, Y, Z uint64
}

func (v *d08Vector3) Dist(other d08Vector3) uint64 {
	dx := v.X - other.X
	dy := v.Y - other.Y
	dz := v.Z - other.Z
	return dx*dx + dy*dy + dz*dz
}

type d08Dist struct {
	Dist uint64
	A, B d08Vector3
}

type d08 struct{}

func (d d08) run(r io.Reader) aoc.Result {
	points, err := d.parse(r)
	if err != nil {
		return aoc.Error(err)
	}

	dists := &d08Distances{}
	for i, point := range points {
		for _, other := range points[i+1:] {
			heap.Push(dists, &d08Dist{
				Dist: point.Dist(other),
				A:    point,
				B:    other,
			})
		}
	}

	var resultA int
	var resultB uint64

	index := 0
	conns := 0
	groupCount := 0
	groups := map[d08Vector3]int{}
	for {
		dist := heap.Pop(dists).(*d08Dist)

		// part a
		if conns == 1000 {
			counts := make([]int, index)
			for _, group := range groups {
				counts[group-1] += 1
			}
			slices.Sort(counts)
			resultA = 1
			for _, count := range counts[:3] {
				resultA *= count
			}
		}
		conns += 1

		aGroup := groups[dist.A]
		bGroup := groups[dist.B]
		switch {
		case aGroup == 0 && bGroup == 0:
			index++
			groupCount += 1
			groups[dist.A] = index
			groups[dist.B] = index

		case aGroup == 0:
			groups[dist.A] = bGroup

		case bGroup == 0:
			groups[dist.B] = aGroup

		case aGroup != bGroup:
			groupCount -= 1
			for key, group := range groups {
				if group == bGroup {
					groups[key] = aGroup
				}
			}

		default:
			continue
		}

		// part b
		if groupCount == 1 && len(groups) == len(points) {
			resultB = dist.A.X * dist.B.X
			break
		}
	}

	return aoc.Solution(resultA, resultB)
}

var _ heap.Interface = (*d08Distances)(nil)

type d08Distances []*d08Dist

func (d *d08Distances) Len() int {
	return len(*d)
}

func (d *d08Distances) Less(i, j int) bool {
	return (*d)[i].Dist < (*d)[j].Dist
}

func (d *d08Distances) Swap(i, j int) {
	(*d)[i], (*d)[j] = (*d)[j], (*d)[i]
}

func (d *d08Distances) Push(a any) {
	*d = append(*d, a.(*d08Dist))
}

func (d *d08Distances) Pop() any {
	last := len(*d)
	val := (*d)[last-1]
	*d = (*d)[:last-1]
	return val
}

func (d d08) parse(r io.Reader) ([]d08Vector3, error) {
	var points []d08Vector3

	scanner := bufio.NewScanner(r)
	for scanner.Scan() {
		line := scanner.Text()
		a, after, found := strings.Cut(line, ",")
		if !found {
			continue
		}
		b, c, found := strings.Cut(after, ",")
		if !found {
			continue
		}
		x, err := strconv.ParseUint(a, 10, 64)
		if err != nil {
			return nil, err
		}
		y, err := strconv.ParseUint(b, 10, 64)
		if err != nil {
			return nil, err
		}
		z, err := strconv.ParseUint(c, 10, 64)
		if err != nil {
			return nil, err
		}
		points = append(points, d08Vector3{
			X: x,
			Y: y,
			Z: z,
		})
	}
	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return points, nil
}
