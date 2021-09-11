import os
import time
import json
import telebot
from gtts import gTTS

# Reads the token from the JSON
f = open('token.json')
TOKEN = json.load(f)
TOKEN = TOKEN["TOKEN"]


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["siri_start","siri_help"])
def help(message):
    message_to_be_sent = "/siri_start - Lists commands\n"
    message_to_be_sent += "/siri_help - Lists commands\n"
    message_to_be_sent += "/repo - Link to github repository"
    message_to_be_sent += "/talk <text> - Bot says <text>\n"
    message_to_be_sent += "/siri_status\n"
    bot.send_message(message.chat.id, message_to_be_sent)


@bot.message_handler(commands=['repo'])
def handle_talk(message):
	bot.send_message(message.chat.id, "https://github.com/AlbFR/Telegram-Voice-Bot")

@bot.message_handler(commands=['talk'])
def handle_talk(message):

	print(message.chat.id)
	print("The message was: ", message.text)
	usr_id = message.from_user.id
	usr_id = str(usr_id)
	message.text = message.text[::-1][:-6][::-1] # erases the "/talk "
	print(message.text)
	print("Message sent by: ", message.from_user.first_name)
	audio_path = "audiofiles/"+usr_id+"."
	createAudio(message.text, audio_path)
	time.sleep(1)
	cmd = "ffmpeg -y -i " + audio_path
	cmd += "mp3 -c:a libopus -b:a 8k " + audio_path
	cmd += "ogg"
	os.system(cmd) # Parses the .mp3 onto .ogg (format of telegram voice)
	bot.send_voice(message.chat.id, open(audio_path+"ogg", 'rb'))

@bot.message_handler(commands=["siri_status"])
def handle_status(message):
    bot.send_message(message.chat.id, "Ando de la maraca hmno")
	
def createAudio(text, path):
	audio = gTTS(text, lang="es", tld="com.mx")
	audio.save(path+"mp3")


os.system("rm -r audiofiles")
os.system("mkdir audiofiles")

bot.polling(timeout=5)