package aoc

import (
	"encoding/json"
	"fmt"
	"io"
)

type Solver func(io.Reader) Result

type Result interface {
	Serialize() []byte
	result()
}

func Solution(a, b any) Result {
	return &solution{a, b}
}

var _ Result = (*solution)(nil)

type solution struct {
	A any
	B any
}

func (r *solution) Serialize() []byte {
	result := []byte("value:[")

	if r.A != nil {
		val, _ := json.Marshal(fmt.Sprintf("%v", r.A))
		result = append(result, val...)
	} else {
		result = append(result, "null"...)
	}

	result = append(result, ","...)

	if r.B != nil {
		val, _ := json.Marshal(fmt.Sprintf("%v", r.B))
		result = append(result, val...)
	} else {
		result = append(result, "null"...)
	}

	return append(result, "]"...)
}

func (*solution) result() {}

func StrError(err string) *ErrorResult {
	return &ErrorResult{err}
}

func Error(err error) *ErrorResult {
	return &ErrorResult{err.Error()}
}

var _ Result = (*ErrorResult)(nil)

type ErrorResult struct {
	msg string
}

func (r *ErrorResult) Serialize() []byte {
	val, _ := json.Marshal(r.msg)
	return append([]byte("error:"), val...)
}

func (*ErrorResult) result() {}
