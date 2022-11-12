# Robin, the Scale Tipper
A Discord Bot written in Golang, he is the prime tactition of the FEH-Gauntlet-Bot Army.

## Features
* Converts Twitter messages to Atemosta Nitter Instance 
* MongoDB Integration

## Invite Robin Bot to Server
Paste the following url in the browser to invite the client to your server (will ask for admin permissions).
[https://discord.com/api/oauth2/authorize?client_id=1040424451638050887&permissions=8&scope=bot](https://discord.com/api/oauth2/authorize?client_id=1040424451638050887&permissions=8&scope=bot)

Make sure you enable `Message Intent` in **Discord Developer Bot Settings**

## Setting Up
1. Install Go via [https://dev.to/aurelievache/learning-go-by-examples-introduction-448n](https://dev.to/aurelievache/learning-go-by-examples-introduction-448n)
2. `go mod init golang-discord-bot-robin` ->  Create a go.mod file init.
3. `go mod tidy` ->  Just a requirement.
4. `go get "github.com/bwmarrin/discordgo" ` -> Package which we will be using to create our discord bot in Golang.

## Start the Bot
### Using Docker Compose and config.json
```
cp config.json.example config.json 
docker-compose up -d
```
### Using Environment Variables
```
export BOT_TOKEN=<<BOT_TOKEN>>
go run main.go -t $BOT_TOKEN
```