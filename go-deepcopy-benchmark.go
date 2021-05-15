package main

import (
	"bytes"
	"encoding/gob"
	"encoding/json"
	"log"
	"time"

	"strconv"
)

// Test ...
type Test struct {
	Prop1 int
	Prop2 string
}

// Clone deep-copies a to b
func Clone(a, b interface{}) {
	buff := new(bytes.Buffer)
	enc := gob.NewEncoder(buff)
	dec := gob.NewDecoder(buff)
	enc.Encode(a)
	dec.Decode(b)
}

// DeepCopy deepcopies a to b using json marshaling
func DeepCopy(a, b interface{}) {
	byt, _ := json.Marshal(a)
	json.Unmarshal(byt, b)
}

// ClonePointer deepcopies a to b using json marshaling
func ClonePointer(a, b *Test) {
	b = &Test{
		Prop1: a.Prop1,
		Prop2: a.Prop2,
	}
}

// CloneNonPointer deepcopies a to b using json marshaling
func CloneNonPointer(a, b Test) {
	b = Test{
		Prop1: a.Prop1,
		Prop2: a.Prop2,
	}
}

func main() {
	i := 0
	tClone := time.Duration(0)
	tCopy := time.Duration(0)
	tClonePointer := time.Duration(0)
	tCloneNonPointer := time.Duration(0)
	round := 3000
	for {
		if i == round {
			break
		}

		r := Test{Prop1: i, Prop2: strconv.Itoa(i)}
		var rNew Test
		t0 := time.Now()
		Clone(r, &rNew)
		t2 := time.Now().Sub(t0)
		tClone += t2

		r2 := Test{Prop1: i, Prop2: strconv.Itoa(i)}
		var rNew2 Test
		t0 = time.Now()
		DeepCopy(&r2, &rNew2)
		t2 = time.Now().Sub(t0)
		tCopy += t2

		r3 := &Test{Prop1: i, Prop2: strconv.Itoa(i)}
		var rNew3 *Test
		t0 = time.Now()
		ClonePointer(r3, rNew3)
		t2 = time.Now().Sub(t0)
		tClonePointer += t2

		r4 := Test{Prop1: i, Prop2: strconv.Itoa(i)}
		var rNew4 Test
		t0 = time.Now()
		CloneNonPointer(r4, rNew4)
		t2 = time.Now().Sub(t0)
		tCloneNonPointer += t2

		i++
	}
	log.Printf("Total items %+v, Clone avg. %+v, DeepCopy avg. %+v, ClonePointer avg. %+v, CloneNonPointer avg. %+v\n", i, int(tClone.Nanoseconds())/round, int(tCopy.Nanoseconds())/round, int(tClonePointer.Nanoseconds())/round, int(tCloneNonPointer.Nanoseconds())/round)
}
