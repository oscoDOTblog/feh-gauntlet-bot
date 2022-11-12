package bot

import (
   "fmt" //to print errors
   "golang-discord-bot/config" //importing our config package which we have created above
   "github.com/bwmarrin/discordgo" //discordgo package from the repo of bwmarrin . 
	 "strings"
)

var BotId string
var goBot *discordgo.Session

func Start() {

	//creating new bot session
	goBot, err := discordgo.New("Bot " + config.Token)

	//Handling error
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	// Making our bot a user using User function .
	u, err := goBot.User("@me")
	//Handling error
	if err != nil {
		fmt.Println(err.Error())
		return
	}
	// Storing our id from u to BotId .
	BotId = u.ID

	// Adding handler function to handle our messages using AddHandler from discordgo package. We will declare messageHandler function later.
	goBot.AddHandler(setPresence)
	goBot.AddHandler(messageHandler)

	err = goBot.Open()
	//Error handling
	if err != nil {
		fmt.Println(err.Error())
		return
	}
		//If every thing works fine we will be printing this.
	fmt.Println("Bot is running !")
	}

	// Set Bot Activity
	func setPresence(s *discordgo.Session, event *discordgo.Ready) {
		s.UpdateGameStatus(0,"Fire Emblem: Awakening")
	}

	//Definition of messageHandler function it takes two arguments first one is discordgo.Session which is s , second one is discordgo.MessageCreate which is m.
	func messageHandler(s *discordgo.Session, m *discordgo.MessageCreate) {
		//Bot musn't reply to it's own messages , to confirm it we perform this check.
	if m.Author.ID == BotId {
		return
	}

	// Health Check commands
	if m.Content == "owo" {
		_, _ = s.ChannelMessageSend(m.ChannelID, "uwu")
	}
	if m.Content == "uwu" {
		_, _ = s.ChannelMessageSend(m.ChannelID, "owo")
	}
	if m.Content == "kuma" || m.Content == "bear" || m.Content == "oso" {
		_, _ = s.ChannelMessageSend(m.ChannelID, "ʕ •ᴥ•ʔ")
	}

	// Time to tip the scales! 
	if m.Content == config.BotPrefix + "time" || m.Content == config.BotPrefix + "scales" || m.Content == "What time is it?" {
		_, _ = s.ChannelMessageSend(m.ChannelID, "Time to tip the scales!")
	}

	// Convert Twitter links to ATOS Nitter Instance
	if strings.Contains(m.Content, "twitter.com") {
		_, _ = s.ChannelMessageSend(m.ChannelID, "`Converted to Atemosta's Nitter Instance 🪄`\n" + strings.Replace(m.Content, "twitter.com", "nitter.atemosta.com", -1))
	}

	// fmt.Println("It's Pizza Time")
	// fmt.Println(config.BotPrefix)

	//If we message ping to our bot in our discord it will return us pong .
	if m.Content == "ping" {
		_, _ = s.ChannelMessageSend(m.ChannelID, "pong")
	}
}