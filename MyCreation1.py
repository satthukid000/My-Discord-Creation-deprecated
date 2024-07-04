# This example requires the 'message_content' intent.
import discord
import random
import os
from dotenv import load_dotenv
import functions
import db.UserList as DefaultUserList
import google.generativeai as genai
import time

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
API_KEY = os.getenv("GOOGLE_CLOUD_KEY")
genai.configure(api_key=API_KEY)

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # print(message)
    if message.author == client.user:
        return
    greetings = ["hello", "hi", "xin chào", "chào buổi", "ali", "alo"]
    bots_creation1_name = ["creation 1", "creation số 1", "creation no 1"]
    #Những điều cơ bản bình thường
    ## Cần cải thiện sau
    # if functions.contains_substring(message.content.lower(), greetings):
    #     response = functions.get_random_response("OnGreeting.txt")
    #     formatted_response = response.replace("{message.author.mention}", message.author.mention)
    #     await message.channel.send(formatted_response)
    #     print(f'{message.author.mention} said Greeting so I greeted them')
    stop_flag = False
        
    #Kiểm tra message NSFW
        
    # Ai đó nhắc đến bot
    for mentioned_user in message.mentions:
        if mentioned_user == message.guild.me and message.author.id != functions.user_cr_2['user_id']: 
            response = functions.get_random_response("OnMentioned.txt")
            formatted_response = response.replace("{message.author.mention}", message.author.mention)
            await message.channel.send(formatted_response)
            print(f'{message.author.mention} mentioned me')
            
    if functions.contains_substring(message.content.lower(), bots_creation1_name):
        flag, mess = await functions.check_message_nsfw(message, client)
        if flag != 0:
            await message.channel.send(mess)
        else:
            time.sleep(4)
            model = genai.GenerativeModel('gemini-1.5-flash', functions.safety_settings)
            prompt = functions.get_proper_prompt(message,"Creation 1")
            print(f"Prompt generated from {client.user}: {prompt}")
            response = model.generate_content(f"{prompt}")
            await message.channel.send(f"{message.author.mention} {response.text}")
            print(f"Username {message.author.name}, Display user name {message.author.display_name} directly call {client.user}")
            time.sleep(4)

bot_token = os.getenv("BOT_TOKENN")
client.run(bot_token)