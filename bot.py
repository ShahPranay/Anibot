import os
from discord import Member,Embed,ext
from typing import Optional
import random
import requests
import re

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

@bot.command(name='anidex', help="Prints the details of an anime.")
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
            seasonYear
            coverImage{
                large
            }
            rankings{
                rank
                allTime
                type
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
    idstr=str(data["data"]["Media"]["id"])
    if(data["data"]["Media"]["title"]["english"] is not None): 
        tit=data["data"]["Media"]["title"]["english"]+"\n"+data["data"]["Media"]["title"]["romaji"]
    else:
        tit=data["data"]["Media"]["title"]["romaji"]
    embedVar=Embed(title=tit, url="https://anilist.co/anime/"+idstr)
    if(data["data"]["Media"]["coverImage"]["large"] is not None):
        embedVar.set_image(url=data["data"]["Media"]["coverImage"]["large"])
    if(type(data["data"]["Media"]["description"] is not None)):
        html=markdown(data["data"]["Media"]["description"])
        soup = BeautifulSoup(html, "html.parser")
        text=soup.get_text()
        if(len(text)>1024):    
            text=text[:1020]+"..."
        embedVar.add_field(name="Synopsis:", value=text, inline=False)
    if(data["data"]["Media"]["status"] is not None):
        embedVar.add_field(name="Staus:", value=data["data"]["Media"]["status"].lower(), inline=True)
    if(data["data"]["Media"]["episodes"] is not None):
        embedVar.add_field(name="Episode Count:", value=data["data"]["Media"]["episodes"], inline=True)
    if(data["data"]["Media"]["meanScore"] is not None):
        embedVar.add_field(name="Mean Score:", value=data["data"]["Media"]["meanScore"], inline=True)
    if(data["data"]["Media"]["seasonYear"] is not None):
        embedVar.add_field(name="Release Year:", value=data["data"]["Media"]["seasonYear"], inline=True)
    if(len(data["data"]["Media"]["rankings"])!=0):
        s2=""
        for item in data["data"]["Media"]["rankings"]:
            if item["allTime"]:
                if(item["type"]=="RATED"):
                    s1="User ratings\n"
                else:
                    s1="Popularity\n"
                s2+="#"+str(item["rank"])+" in all Time " + s1
        embedVar.add_field(name="Rankings:", value=s2, inline=False)    
    #tags
    taglst=[]
    for item in data["data"]["Media"]["tags"]:
        if(not item["isMediaSpoiler"]):
            taglst.append(item["name"])
    if(not len(taglst)==0):
        embedVar.add_field(name="Tags:", value=", ".join(taglst), inline=False)

    #stream url
    streamurl="https://animixplay.to/?q="
    if (sq:=data["data"]["Media"]["title"]["english"]) is not None:
        searchquery=sq.lower()
    else:
        searchquery=data["data"]["Media"]["title"]["romaji"].lower()
    searchquery=searchquery.split(" ")
    searchquery="%20".join(searchquery)
    streamurl+=searchquery
    embedVar.add_field(name="Stream From:",value=streamurl, inline=False)

    await ctx.send(embed=embedVar)

@bot.command(name='mangadex', help="Prints the details of a manga.")
async def manga_title(ctx, *,name):
    query='''
    query($manname: String){
        Media (search: $manname, type: MANGA){
            id
            title {
                romaji
                english
            }
            status
            description
            chapters
            volumes
            meanScore
            tags{
                name
                isMediaSpoiler
            }
            seasonYear
            coverImage{
                large
            }
            rankings{
                rank
                allTime
                type
            }
        }
    }
    '''
    variables = {
        'manname': name
    }
    url = 'https://graphql.anilist.co'
    response = requests.post(url, json={'query': query, 'variables': variables})
    data = response.json()
    if("errors" in data):
        for item in data["errors"]:
            await ctx.send(item["message"])
        return
    idstr=str(data["data"]["Media"]["id"])
    if(data["data"]["Media"]["title"]["english"] is not None): 
        tit=data["data"]["Media"]["title"]["english"]+"\n"+data["data"]["Media"]["title"]["romaji"]
    else:
        tit=data["data"]["Media"]["title"]["romaji"]
    embedVar=Embed(title=tit, url="https://anilist.co/anime/"+idstr)
    if(data["data"]["Media"]["coverImage"]["large"] is not None):
        embedVar.set_image(url=data["data"]["Media"]["coverImage"]["large"])
    if(type(data["data"]["Media"]["description"] is not None)):
        html=markdown(data["data"]["Media"]["description"])
        soup = BeautifulSoup(html, "html.parser")
        text=soup.get_text()
        if(len(text)>1024):    
            text=text[:1020]+"..."
        embedVar.add_field(name="Synopsis:", value=text, inline=False)
    if(data["data"]["Media"]["status"] is not None):
        embedVar.add_field(name="Staus:", value=data["data"]["Media"]["status"].lower(), inline=True)
    if(data["data"]["Media"]["chapters"] is not None):
        embedVar.add_field(name="Chapter Count:", value=data["data"]["Media"]["chapters"], inline=True)
    if(data["data"]["Media"]["volumes"] is not None):
        embedVar.add_field(name="Volume Count:", value=data["data"]["Media"]["volumes"], inline=True)

    if(data["data"]["Media"]["meanScore"] is not None):
        embedVar.add_field(name="Mean Score:", value=data["data"]["Media"]["meanScore"], inline=True)
    if(data["data"]["Media"]["seasonYear"] is not None):
        embedVar.add_field(name="Release Year:", value=data["data"]["Media"]["seasonYear"], inline=True)
    if(len(data["data"]["Media"]["rankings"])!=0):
        s2=""
        for item in data["data"]["Media"]["rankings"]:
            if item["allTime"]:
                if(item["type"]=="RATED"):
                    s1="User ratings\n"
                else:
                    s1="Popularity\n"
                s2+="#"+str(item["rank"])+" in all Time " + s1
        embedVar.add_field(name="Rankings:", value=s2, inline=False)    
    
    #tags
    taglst=[]
    for item in data["data"]["Media"]["tags"]:
        if(not item["isMediaSpoiler"]):
            taglst.append(item["name"])
    if(not len(taglst)==0):
        embedVar.add_field(name="Tags:", value=", ".join(taglst), inline=False)
    readurl="https://manganelo.com/search/story/"
    if(data["data"]["Media"]["title"]["english"] is not None): 
        urlname=data["data"]["Media"]["title"]["english"]
    else:
        urlname=data["data"]["Media"]["title"]["romaji"]
    urlname=re.split("'| ",urlname)
    urlname="_".join(urlname)
    readurl+=urlname
    embedVar.add_field(name="Stream From:",value=readurl, inline=False)
    await ctx.send(embed=embedVar)



@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, ext.commands.CommandNotFound):
        print("The enterd command does not exist.Type !help to know existing commands.")
    else:
        print(error)

bot.run(TOKEN)