import os
import discord
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
client.run(TOKEN)