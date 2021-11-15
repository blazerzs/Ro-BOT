import discord
from discord.ext import commands
from discord import Embed, File
import os
import asyncio
import datetime
from datetime import timedelta
import time
import typing
import giphy_client
from giphy_client.rest import ApiException
import random
from discord.utils import get
from keep_alive import keep_alive
from discord.ext.commands import is_owner
from discord.ext import tasks
from itertools import cycle

intents = discord.Intents.all()
client = commands.Bot(command_prefix=".",
                      case_insensitive=True,
                      help_command=None,
                      intent=intents)

@client.command()
async def ping(ctx):
  await ctx.channel.send(f"Hello! My current ping is {round(client.latency*1000)} ms.")

@client.command(aliases=['commands', 'cmds', 'help'])
async def command(ctx):
  author_name = ctx.message.author.name

  embed = discord.Embed(
    title=":crayon: MY COMMANDS", 
    description=f"Hey there {author_name}, welcome to your group! Below you can locate all my commands! \n \n Group Link: https://www.roblox.com/groups/ \n Prefix: . \n", 
    colour=0xda9e34)

  embed.add_field(name='🚨 ; Moderation', value='``` .blacklist \n .kick \n .ban \n .banlog \n .blacklistlog```', inline=False)
  embed.add_field(name='🕵 ; Internal Affairs', value='``` .new \n .close \n .case \n .alert \n .caselog```', inline=True)
  embed.add_field(name='🦺 ; Appeals', value='``` .termapp \n .demoapp \n .strikeapp \n .suspendapp```', inline=False)
  embed.add_field(name='💼 ; Staff Management', value='```N/A ; No commands currently```', inline=True)
  embed.add_field(name='🤝 ; Public Relations', value='``` .allianceannounce (Main Server only)```', inline=False)


  embed.set_thumbnail(url='https://image.com')
  embed.set_footer(text = "Made by (your name)")
  
  await ctx.author.send(embed=embed)
  await ctx.send(f":crayon: ; {ctx.message.author.mention}, check your dms!")

#moderation

@client.command()
@commands.has_permissions(ban_members=True)
async def blacklist(ctx, user: discord.Member, *, reason):
  
  author_name = ctx.message.author.mention

  embed = discord.Embed(
    title=":crayon: : BLACKLIST SYSTEM", 
    description=f"Hey there! You have been blacklisted from group name for the reasons which can be located within the following text!", 
    colour=0xda9e34)

  embed.add_field(name=':hammer: ; BLACKLISTED BY:', value=f'{author_name}', inline=True)
  embed.add_field(name=':rotating_light: ; REASONING', value=f'{reason}', inline=False)

  embed.set_thumbnail(url='https://image.com')
  embed.set_footer(text = "Department Manager ; Made by (your name)")
  
  await user.send(embed=embed)
  await ctx.send(f":crayon: ; Successfully blacklisted {user}.")
  for guild in client.guilds:
    await guild.ban(user)

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member, *,reason= "Uh Oh! No reason provided."):
  await member.send(f"You were kicked from {ctx.guild.name}! Reasoning: " +reason)
  await ctx.channel.send(f"{ctx.message.author.name} has kicked {member} for: "+reason )
  await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member, *,reason= "Uh Oh! No reason provided."):
  await member.send(f"Uh Oh! You were banned from {ctx.guild.name}! Reasoning: " +reason)
  await ctx.channel.send(f"{ctx.message.author.name} has banned {member} for: "+reason )
  await member.ban(reason=reason)

@client.command() 
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_descriminator = member.split('#')

  for ban_entry in banned_users: 
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_descriminator):
      await ctx.guild.unban(user)
      await ctx.send(f'Unbanned {user.mention}')
      return

@client.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, user: discord.Member, *, dm):

  embed = discord.Embed(
    title=":crayon: : LPD MESSAGE SYSTEM", 
    description=f"Leaking this message may result in a blacklist if deemed important.", 
    colour=0xda9e34)

  embed.add_field(name=':rotating_light: ; MESSAGE', value=f'{dm}', inline=False)

  embed.set_thumbnail(url='https://image.com')
  embed.set_footer(text = "Department Manager ; Made by (your name)")
  
  await user.send(embed=embed)
  await ctx.send(f":crayon: ; Successfully direct messaged {user}.")

#internal affairs

@client.command()
@commands.has_permissions(ban_members=True)
async def caseintro(ctx, *, reason):
  embed = discord.Embed(
    title=":crayon: : INTERNAL AFFAIRS", 
    description=f"Admirations, on behalf of the Internal Affairs department I thank you for being here and taking the time to assist us in efficiently bringing this case to a conclusion. \n The IA staff member(s) will explain this case further, rhe reasoning for this will be stated below please ensure you are cooperating with our staff team to ensure the best outcome is reached for your behalf.", 
    colour=0xda9e34)

  embed.add_field(name=':hammer: ; REASONING', value=f'{reason}', inline=True)
  embed.add_field(name=':rotating_light: ; THANK YOU', value=f'\n If you have any questions, ensure  as them below as the IA staff member will be here to deal with your case until a active conclusion is found.', inline=False)

  embed.set_thumbnail(url='https://image.com')
  embed.set_footer(text = "Department Manager ; Made by (your name)")
  
  await ctx.send(embed=embed)

  
  

# appeals

# staff management

# public relations

# logging

@client.command()
@commands.has_permissions(ban_members=True)
async def plog(ctx, user, *, reason):
  
  author_name = ctx.message.author.mention

  embed = discord.Embed(
    title=":crayon: : NEW PROMOTION", 
    description=f"", 
    colour=0xda9e34)

  embed.add_field(name=':briefcase: ; PROMOTED BY:', value=f'{author_name}', inline=True)
  embed.add_field(name=':crayon: ; USERNAME:', value=f'{user}', inline=False)
  embed.add_field(name=':angel: ; REASON:', value=f'{author_name}', inline=True)

  embed.set_thumbnail(url='https://image.com')
  embed.set_footer(text = "Department Manager ; Made by (your name)")
  
  await ctx.send(f":crayon: ; Successfully blacklisted {user}.")





# other commands

@client.event
async def on_command_error(ctx, error):
  await ctx.channel.send(error)
  print("command exception", type(error), error)

status = cycle(['Welcome to (your group)', 'https://www.roblox.com/groups/', '.help'])

@client.event
async def on_ready():
  change_status.start()
  print('{0.user}'.format(client))
  print('Is Online')

@tasks.loop(seconds=30)
async def change_status():
  await client.change_presence(activity=discord.Game(next(status)))

  

@client.command()
async def sleep(ctx):
    id = str(ctx.author.id)
    if id == '1':
        message = await ctx.send(':crayon: ;; Okok! Brushing my teeth! :)')
        await asyncio.sleep(3) 
        await message.edit(content='Getting Changed.')
        await asyncio.sleep(1)
        await message.edit(content='Tucking Myself In..')
        await asyncio.sleep(1)
        await message.edit(content='Closing My Eyes...')
        await asyncio.sleep(1)
        await message.edit(content=':bed: ;; I will no longer respond until reactivated.')
        await asyncio.sleep(1)
        await ctx.bot.logout()
    else:
        await ctx.send(":rage: ;; HEY! You cant tell me what to do!!")

keep_alive()
client.run(os.getenv("TOKEN"))