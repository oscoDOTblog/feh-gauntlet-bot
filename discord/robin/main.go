package main

import (
  "fmt"
  "golang-discord-bot/bot" //we will create this later
  "golang-discord-bot/config" //we will create this later
) 

func main() {
  err := config.ReadConfig()

  if err != nil {
  	fmt.Println(err.Error())
  	return
  }

  bot.Start()

  <-make(chan struct{})
  return
}