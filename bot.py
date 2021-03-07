import os
from discord import Member,Embed
from typing import Optional
import random
import requests

from discord.ext import commands
from discord.ext.commands import BadArgument
from bs4 import BeautifulSoup
from markdown import markdown

#intents = discord.Intents.default()
#intents.members = True
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#client = discord.Client(intents=intents)
bot= commands.Bot(command_prefix="!")

@bot.command(name='anidex')
async def anime_title(ctx, *,name):
    query='''
    query($aniname: String){
        Media (search: $aniname, type: ANIME){
            id
            title {
                romaji
                english
            }
            status
            description
            episodes
            meanScore
            tags{
                name
                isMediaSpoiler
            }
        }
    }
    '''
    variables = {
        'aniname': name
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    if("errors" in data):
        for item in data["errors"]:
            await ctx.send(item["message"])
        return
    if(data["data"]["Media"]["title"]["english"] is not None): 
        tit=data["data"]["Media"]["title"]["english"]+"\n"+data["data"]["Media"]["title"]["romaji"]
    else:
        tit=data["data"]["Media"]["title"]["romaji"]
    embedVar=Embed(title=tit)
    if(type(data["data"]["Media"]["description"] is not None)):
        html=markdown(data["data"]["Media"]["description"])
        soup = BeautifulSoup(html, "html.parser")
        text=soup.get_text()
        embedVar.add_field(name="Synopsis:", value=text, inline=False)
    if(data["data"]["Media"]["status"] is not None):
        embedVar.add_field(name="Staus:", value=data["data"]["Media"]["status"].lower(), inline=True)
    if(data["data"]["Media"]["episodes"] is not None):
        embedVar.add_field(name="Episode Count:", value=data["data"]["Media"]["episodes"], inline=True)
    if(data["data"]["Media"]["meanScore"] is not None):
        embedVar.add_field(name="Mean Score:", value=data["data"]["Media"]["meanScore"], inline=True)
    taglst=[]
    for item in data["data"]["Media"]["tags"]:
        if(not item["isMediaSpoiler"]):
            taglst.append(item["name"])
    if(not len(taglst)==0):
        embedVar.add_field(name="Tags:", value=", ".join(taglst), inline=True)
    await ctx.send(embed=embedVar)


bot.run(TOKEN)