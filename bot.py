import os
import traceback
import time
import json
import telebot
from gtts import gTTS

f = open('info.json')
info_file = json.load(f)
TOKEN = info_file["TOKEN"]
inf_id = info_file["inf_id"]
f.close()

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["siri_start","siri_help"])
def help(message):
	message_to_be_sent = "/siri_start - Lists commands\n"
	message_to_be_sent += "/siri_help - Lists commands\n"
	message_to_be_sent += "/repo - Link to github repository\n"
	message_to_be_sent += "/talk <text> - Bot says <text>\n"
	message_to_be_sent += "/siri_status\n"
	bot.send_message(message.chat.id, message_to_be_sent)


@bot.message_handler(commands=['repo'])
def handle_talk(message):
	bot.send_message(message.chat.id, "https://github.com/AlbFR/Telegram-Voice-Bot")


@bot.message_handler(commands=['talk'])
def handle_talk(message):

	# print("Chat ID:", message.chat.id)
	if message.chat.title != None:
		print("Group:",message.chat.title)

	msg = message.text[::-1][:-6][::-1] # ignores the "/talk "
	print('"'+msg+'"')
	print(message.from_user.first_name+":", msg)
	print("o-----------------------o")

	# For fun purposes xd
	# If u understand how to use it, use it properly
	inf = False
	if msg[:4] == "inf_":
		inf = True
		msg = msg[::-1][:-4][::-1]

	usr_id = message.from_user.id
	usr_id = str(usr_id)
		
			
	audio_path = "audiofiles/"+usr_id+"."
	print(createAudio(msg, audio_path))
	if createAudio(msg, audio_path):
		print("flag2")	
		time.sleep(1)

		cmd = "ffmpeg -nostats -loglevel 0 -y -i " + audio_path
		cmd += "mp3 -c:a libopus -b:a 8k " + audio_path
		cmd += "ogg"
		os.system(cmd) # Parses the .mp3 to .ogg (format of telegram voice)

		audio = open(audio_path+"ogg", 'rb')

		try:
			if inf == True:
				bot.send_voice(inf_id, audio)
			else:
				bot.send_voice(message.chat.id, audio)
		except:
			print("An error has occured trying to send the audio :/")
	else:
		print("flag")
		bot.send_message(message.chat.id, "Escribe algo que pueda decir -.-")	

@bot.message_handler(commands=["siri_status"])
def handle_status(message):
	bot.send_message(message.chat.id, "Ando de la maraca hmno")

def createAudio(text, path):
	if text == "":
		return False
	try:
		audio = gTTS(text, lang="es", tld="cl")
		audio.save(path+"mp3")
		return True
	except AssertionError:
		print("Unreadable message :/")
		traceback.print_exc()
		return False
	except:
		pass

def main():
	os.system("rm -r audiofiles")
	time.sleep(0.5)
	os.system("mkdir audiofiles")
	try:
		print("Bot running...")
		bot.polling(timeout=5)
	except KeyboardInterrupt:
		print('[!] Exiting')	
		exit(1)
	except:
		print("\nAn error has occured :/")
		traceback.print_exc()
		print('[!] Exiting')	
		exit(1)

if __name__ == "__main__":
	main()
