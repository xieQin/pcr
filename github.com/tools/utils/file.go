package utils

import (
	"fmt"
	"log"
	"os"
)

// ReadFile func
func ReadFile(path string, bytes int32) []byte {
	fp, err := os.OpenFile(path, os.O_RDONLY, 0755)
	defer fp.Close()
	if err != nil {
		log.Fatal(err)
	}
	data := make([]byte, bytes)
	n, err := fp.Read(data)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(string(data[:n]), " read file res")
	return data[:n]
}

// WriteFile func
func WriteFile(path string, data []byte) {
	fp, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE, 0755)
	if err != nil {
		log.Fatal(err)
	}
	defer fp.Close()
	_, err = fp.Write(data)
	if err != nil {
		log.Fatal(err)
	}
}
