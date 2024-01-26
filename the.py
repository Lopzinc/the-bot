import discord
from discord.ext import commands
import random
import time
import json
import asyncio
import os



intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='', intents=intents)



try:
    with open('C:/Users/owene/Desktop/the bot/stats/msg.json', 'r') as file:
        scores = json.load(file)
except FileNotFoundError:
    scores = {}







async def save_scores():
    with open('C:/Users/owene/Desktop/the bot/stats/msg.json', 'w') as file:
        json.dump(scores, file)



async def sendPos(message, sorted_scores, rankings_message, user_id_original):
    
    the_score = None
    adjusted_ranking = 0
    
    for idx, (user_id, score) in enumerate(sorted_scores, 1):
        user = bot.get_user(int(user_id))
        position = ""
        botmsg = ""
        
        if user and user.name.lower() == "the":
            the_score = score
            adjusted_ranking = idx
            continue
        
        if idx == 1:
            position = ":first_place:"
        elif idx == 2:
            position = ":second_place:" if the_score else ":third_place:"
        elif idx == 3:
            position = ":third_place:" if not the_score else ":second_place:"
        else:
            position = f"{idx - 1}." if (idx-1) != 3 else ":third_place:"

        if str(user_id_original) == "1195487691131859035":
            botmsg = f"the: {score}"
        else:
            username = user.name if user else "max"
            rankings_message += f"{position} {username}: {score}\n"
    
    if the_score:
        rankings_message += f"\nthe: {the_score}"
    
    await message.channel.send(rankings_message)
    print(rankings_message)







@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    print(message.author.id)
    user_id = str(message.author.id)
    if message.content != "!click" and str(user_id) != "1158076229887475782":
        scores[user_id] = scores.get(user_id, 0) + 1

        # Save scores to the file
        with open('C:/Users/owene/Desktop/the bot/stats/msg.json', 'w') as file:
            json.dump(scores, file)
    else:
        await click()
    if message.content.lower().startswith("!leavetheserver, this code is really secret and itll leave."):
        guild_id = 1195791273504813206
        guild = discord.utils.get(bot.guilds, id=guild_id)
        await guild.leave()
    elif message.content.startswith("!rate "):
        silent = discord.utils.get(message.guild.roles, name="Silent Mode")
        subject = message.content.split("!rate ")[1]
        for member in message.guild.members:
            rating = random.randint(1, 10)
            print(member)
            if "Silent Mode" in [role.name for role in member.roles]:
                await message.channel.send(f"{member.name} is rated {rating}/10 for {subject}.")
            else:
                await message.channel.send(f"{member.mention} is rated {rating}/10 for {subject}.")
    elif message.content.startswith("!rate"):
        await message.channel.send(f"no subject provided you absolute buffoon")
    elif message.content.lower().startswith("!silent"):
        silent = discord.utils.get(message.guild.roles, name="Silent Mode")
        if not "Silent Mode" in [role.name for role in message.author.roles]:
            await message.channel.send("Silent mode on, you will no longer be pinged from bot commands.")
            await message.author.add_roles(silent)
        else:
            await message.channel.send("Silent mode off, you will now be pinged from bot commands.")
            await message.author.remove_roles(silent)
#    elif message.content.lower().startswith("!send <"):
#        channel = message.content.lower().split("!send <")[1].split(">")[0]
#        print(channel)
#        channel = bot.get_channel(int(message.content.lower().split("!send <")[1].split(">")[0]))
#        msg = message.content.lower().split("> ")[1]
#        await channel.send(f"{msg}")



#                   _/~- STATS -~\_


            
    elif message.content.lower().startswith("!stats "):
        stat = message.content.lower().split("!stats ")[1]
        if stat.startswith("msg") or stat.startswith("message"):
            rankings_message = "💬 Messages sent:\n"
            sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True) 
            await sendPos(message, sorted_scores, rankings_message, message.author.id)
        




                
bot.run()
