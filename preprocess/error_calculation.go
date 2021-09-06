package main

import (
	"bufio"
	"bytes"
	"encoding/csv"
	"fmt"
	"image/color"
	"io/ioutil"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"strings"
	"time"

	tiff "github.com/chai2010/tiff"
)

type similarity struct {
	id    string
	ratio string
}

type bsideData struct {
	id   int
	area int
}

type related struct {
	id      int
	overlap int
}

type singleId struct {
	id          int
	card        int
	overlapping []related
}

type jsonType struct {
	id          int
	bestAccId   int
	numerator   int
	denominator int
}

type accumulatedJsonType struct {
	id                 int
	individualIdString string
}

type returnStringDataType struct {
	id           int
	returnString string
}

func main() {
	if len(os.Args) != 2 {
		panic("Enter a valid dataset name!\nAborting..")
	}

	dataset := os.Args[1:2][0]
	baseUrl := "./data/celltracking_results/" + dataset + "/"
	csvName := "ids.csv"
	idsName := baseUrl + csvName

	var algorithms []string

	if fileExists(idsName) {
		file, _ := os.Open(idsName)
		rdr := csv.NewReader(bufio.NewReader(file))
		rows, _ := rdr.ReadAll()

		for i := range rows {
			if i == 0 {
				continue
			}
			algorithms = append(algorithms, rows[i][1])
		}
		fmt.Println(algorithms)
	} else {
		files, err := ioutil.ReadDir(baseUrl)
		if err != nil {
			log.Fatal(err)
		}
		for _, f := range files {
			if f.IsDir() {
				if f.Name() == "input" {
					continue
				}
				algorithms = append(algorithms, f.Name())
			}
		}
	}

	algoLen := len(algorithms)

	if algoLen < 2 {
		panic("Not enough algorithms for comparison!\nAborting..")
	}

	for i := 0; i < algoLen; i++ {
		for j := i + 1; j < algoLen; j++ {
			outerAlgorithm := algorithms[i]
			innerAlgorithm := algorithms[j]

			// for 01_RES and 02_RES
			for k := 1; k <= 2; k++ {
				fmt.Print("Processing ", outerAlgorithm, " and ", innerAlgorithm, " 0", k, "...")
				start := time.Now()

				writeUrl := baseUrl + strconv.Itoa(i) + "_" + strconv.Itoa(j) +
					"_0" + strconv.Itoa(k) + "_RES.json"

				writeFile, err := os.Create(writeUrl)
				if err != nil {
					log.Fatal(err)
				}

				tifCount := 0
				outerDirName := baseUrl + outerAlgorithm + "/0" + strconv.Itoa(k) + "_RES"
				innerDirName := baseUrl + innerAlgorithm + "/0" + strconv.Itoa(k) + "_RES"

				files, err := ioutil.ReadDir(outerDirName)
				if err != nil {
					log.Fatal(err)
				}
				for _, f := range files {
					if f.Name()[len(f.Name())-4:] == ".tif" {
						tifCount++
					}
				}

				length := len(strconv.Itoa(tifCount))

				var similarityData []returnStringDataType
				c := make(chan returnStringDataType)

				for l := 0; l < tifCount; l++ {
					tifName := "/mask" + strPad(strconv.Itoa(l), length, "0", "LEFT") + ".tif"

					outerTifName := outerDirName + tifName
					innerTifName := innerDirName + tifName

					go tifAccessGoRoutine(strconv.Itoa(l), outerTifName, innerTifName, c)
				}

				for l := 0; l < tifCount; l++ {
					data := <-c

					similarityData = append(similarityData, data)
				}

				sort.Slice(similarityData, func(i, j int) bool {
					return similarityData[i].id < similarityData[j].id
				})

				fmt.Print("Done! Writing to " + writeUrl + "...")

				fmt.Fprintf(writeFile, "{")
				for l := 0; l < tifCount; l++ {
					fmt.Fprintf(writeFile, similarityData[l].returnString)
					if l != tifCount-1 {
						fmt.Fprintf(writeFile, ",")
					}
				}
				fmt.Fprintf(writeFile, "}")

				elapsed := time.Since(start)

				fmt.Println("Done! Took ", elapsed)

				writeFile.Close()
			}
		}
	}

}

func fileExists(directoryName string) bool {
	info, err := os.Stat(directoryName)
	if os.IsNotExist(err) {
		return false
	}
	return !info.IsDir()
}

func strPad(input string, padLength int, padString string, padType string) string {
	var output string

	inputLength := len(input)
	padStringLength := len(padString)

	if inputLength >= padLength {
		return input
	}

	repeat := math.Ceil(float64(1) + (float64(padLength-padStringLength))/float64(padStringLength))

	switch padType {
	case "RIGHT":
		output = input + strings.Repeat(padString, int(repeat))
		output = output[:padLength]
	case "LEFT":
		output = strings.Repeat(padString, int(repeat)) + input
		output = output[len(output)-padLength:]
	case "BOTH":
		length := (float64(padLength - inputLength)) / float64(2)
		repeat = math.Ceil(length / float64(padStringLength))
		output = strings.Repeat(padString, int(repeat))[:int(math.Floor(float64(length)))] + input + strings.Repeat(padString, int(repeat))[:int(math.Ceil(float64(length)))]
	}

	return output
}

func tifAccessGoRoutine(id, outerTifName, innerTifName string, c chan returnStringDataType) {
	convertedId, _ := strconv.Atoi(id)
	if !fileExists(outerTifName) || !fileExists(innerTifName) {
		c <- returnStringDataType{convertedId, "\"" + id + "\":-1"}
		return
	}

	outerData, _ := ioutil.ReadFile(outerTifName)
	innerData, _ := ioutil.ReadFile(innerTifName)

	outerM, _, err := tiff.DecodeAll(bytes.NewReader(outerData))
	if err != nil {
		log.Fatal(err)
	}
	innerM, _, err := tiff.DecodeAll(bytes.NewReader(innerData))
	if err != nil {
		log.Fatal(err)
	}

	rec := outerM[0][0].Bounds()
	outer := outerM[0][0]
	inner := innerM[0][0]

	singleIdSlice := []singleId{}
	bsideMap := make(map[int]int)

	for x := 0; x < rec.Max.X; x++ {
		for y := 0; y < rec.Max.Y; y++ {
			bsideMap[getId(inner.At(x, y))]++
			if getId(outer.At(x, y)) == 0 {
				continue
			}
			singleIdSlice = singleIdExists(singleIdSlice, getId(outer.At(x, y)), getId(inner.At(x, y)))
		}
	}

	// accuracySlice := []jsonType{}
	accuracySlice := []accumulatedJsonType{}

	for _, s := range singleIdSlice {
		sort.Slice(s.overlapping, func(i, j int) bool {
			iOverlap := s.overlapping[i].overlap
			jOverlap := s.overlapping[j].overlap
			return (float64(iOverlap) / float64(s.card+bsideMap[s.overlapping[i].id]-iOverlap)) > (float64(jOverlap) / float64(s.card+bsideMap[s.overlapping[j].id]-jOverlap))
		})

		individualIdSlice := []jsonType{}

		for _, v := range s.overlapping {
			individualIdSlice = append(individualIdSlice, jsonType{
				id:          s.id,
				bestAccId:   v.id,
				numerator:   v.overlap,
				denominator: s.card + bsideMap[v.id] - v.overlap,
			})
		}

		individualIdString := makeIndividualIdString(individualIdSlice)

		accuracySlice = append(accuracySlice, accumulatedJsonType{
			id:                 s.id,
			individualIdString: individualIdString,
		})
	}

	sort.Slice(accuracySlice, func(i, j int) bool {
		return accuracySlice[i].id < accuracySlice[j].id
	})

	idString := makeIdString(accuracySlice)

	returnString := "\"" + id + "\":{" + idString + "}"

	c <- returnStringDataType{convertedId, returnString}
	return
}

func contains(s []color.Color, c color.Color) bool {
	for _, a := range s {
		if a == c {
			return true
		}
	}
	return false
}

func sortedKeys(m map[int]int) []int {
	keys := make([]int, len(m))
	i := 0
	for k := range m {
		keys[i] = k
		i++
	}
	sort.Ints(keys)
	return keys
}

func getId(c color.Color) int {
	r, _, _, _ := c.RGBA()
	return int(r)
}

func singleIdExists(s []singleId, id, targetId int) []singleId {
	for i, v := range s {
		if v.id == id {
			s[i].card++

			if targetId == 0 {
				return s
			}

			updated := false

			for j, u := range s[i].overlapping {
				if u.id == targetId {
					s[i].overlapping[j].overlap++
					updated = true
					break
				}
			}

			if updated {
				return s
			} else {
				newRelatedSingle := related{
					id:      targetId,
					overlap: 1,
				}
				s[i].overlapping = append(s[i].overlapping, newRelatedSingle)
				return s
			}
		}
	}

	newSingleId := singleId{
		id:          id,
		card:        1,
		overlapping: []related{},
	}

	if targetId != 0 {
		newRelatedSingle := related{
			id:      targetId,
			overlap: 1,
		}
		newSingleId.overlapping = append(newSingleId.overlapping, newRelatedSingle)
	}

	s = append(s, newSingleId)

	return s
}

func makeIdString(s []accumulatedJsonType) string {
	idString := ""
	for _, v := range s {
		idString += "\"" + strconv.Itoa(v.id) + "\":" + v.individualIdString + ","
	}
	idString = strings.TrimRight(idString, ",")
	return idString
}

// [[3,254,324],[5,231,645]]
func makeIndividualIdString(s []jsonType) string {
	idString := ""
	for _, v := range s {
		idString += "[" + strconv.Itoa(v.bestAccId) + "," + strconv.Itoa(v.numerator) + "," + strconv.Itoa(v.denominator) + "],"
	}
	idString = "[" + strings.TrimRight(idString, ",") + "]"
	return idString
}
