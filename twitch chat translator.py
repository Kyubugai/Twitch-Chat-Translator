#MADE BY KYBUGAI IN MOST PLATFORMS 
import socket
from translate import Translator
from langdetect import detect

# Twitch settings
print("Made By Kyubugai <3")
print("Twitch Username (The Name of the account you use to translate, you can you the same account as the channel you are translating)")
TWITCH_USERNAME = input("Enter your Twitch username: ")
print("Twitch Channel (The Name of the Channel's Chat you are translating)")
TWITCH_CHANNEL = input("Enter the Twitch channel name: ")
#To get twitch token go to here https://twitchapps.com/tmi/ 
print("To get your Twitch token (DON'T SHARE IT WITH PEOPLE), visit: https://twitchapps.com/tmi/")
TWITCH_TOKEN = input("Enter your Twitch OAuth token (after copying the Token right click the cmd to paste it): ")

# Connect to Twitch chat using WebSockets
s = socket.socket()
s.connect(("irc.chat.twitch.tv", 6667))
s.send(f"PASS {TWITCH_TOKEN}\n".encode())
s.send(f"NICK {TWITCH_USERNAME}\n".encode())
s.send(f"JOIN #{TWITCH_CHANNEL}\n".encode())

# Helper function to send a message to Twitch chat via WebSockets
def send_chat_message(message):
    s.send(f"PRIVMSG #{TWITCH_CHANNEL} :{message}\n".encode())

# Helper function to translate non-English messages using the "translate" library
def translate_message(message):
    try:
        detected_language = detect(message)
        if detected_language != "en":
            translator = Translator(to_lang="en", from_lang=detected_language)
            translated_message = translator.translate(message)
            return translated_message
        return None
    except Exception as e:
        print("Translation error:", e)
        return None

# Main loop to read and translate messages from Twitch chat
while True:
    try:
        BUFFER_SIZE = 2048
        chat_response = s.recv(BUFFER_SIZE).decode()

        if "PRIVMSG" in chat_response:
            parts = chat_response.split(":", 2)
            username = parts[1].split("!", 1)[0]
            message = parts[2]

            if not message.startswith("!"):  # Skip bot commands
                if not message.isascii():  # Check if message is non-English
                    translated_message = translate_message(message)
                    if translated_message is not None:
                        send_chat_message(f"{username}: {translated_message}")
        print("Message Translated.") 
    except Exception as e:
        print(e)
        
