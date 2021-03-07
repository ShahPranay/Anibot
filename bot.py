import os
from discord import Member
from typing import Optional
import random
from discord.ext import commands
from discord.ext.commands import BadArgument

#intents = discord.Intents.default()
#intents.members = True
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#client = discord.Client(intents=intents)
bot= commands.Bot(command_prefix="!")

@bot.command(name='99',help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        )
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)
@bot.command(name='slap', aliases=['hit'],help='slaps person tagged for added reason(optional)')
async def slap_member(ctx, member: Member, *, reason: Optional[str]="for no reason"):
    await ctx.send(f"{ctx.author.display_name} slapped {member.mention} {reason}!")
@slap_member.error
async def slap_member_error(ctx,exc):
    if isinstance(exc, BadArgument):
        await ctx.send("I can't find that member.")

bot.run(TOKEN)