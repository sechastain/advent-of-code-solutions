package main

import (
  "fmt"
  "io/ioutil"
  "os"
  "strings"
  "strconv"
)

func main() {
  ltext, _ := ioutil.ReadFile(os.Args[1])
  lines := strings.Split(string(ltext), "\n")
  lines = lines[0:len(lines)-1]

  depth := 0
  forward := 0

  for _, cmd := range lines {
    parsed := strings.Split(cmd, " ")
    dir := parsed[0]
    dst := parsed[1]
    dist, _ := strconv.Atoi(dst)
    if dir == "forward" {
      forward += dist
    } else if dir == "down" {
      depth += dist
    } else if dir == "up" {
      depth -= dist
    } else {
      fmt.Println("Error - unknown direction: " + dir)
    }
  }

  fmt.Println(len(lines))
  fmt.Println(lines[0])
  fmt.Println(lines[len(lines)-1])

  fmt.Println("----------")

  fmt.Println(depth)
  fmt.Println(forward)
  fmt.Println(depth * forward)

}
