import os
import discord
import random

intents = discord.Intents.default()
intents.members = True
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord!')
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guilds:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    members='\n -'.join([member.name for member in guild.members])
    print(
        f'guild members:\n {members}'
    )
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday!!!🎈🎉')

client.run(TOKEN)