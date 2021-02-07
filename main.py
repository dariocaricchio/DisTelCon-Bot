import keep_alive
import discord
import os
# import requests
# import json
# import lxml
import wikiquote
import random
# import time
import discord.ext
from discord.utils import get
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions,  CheckFailure, check
# from discord.ext.commands import MissingRequiredArgument
from replit import db
import const

'''
To review the application, visit this page:
https://discord.com/developers/applications/805527009530740777/information

To add the bot to one of your servers with default permissions, visit this page:
https://discord.com/api/oauth2/authorize?client_id=805527009530740777&permissions=519232&scope=bot
'''

'''
TODO:
* Update db lang key appending the group_id in order to have different keys instead a single shared key for every server
* Add telegram bot side
* Make discord and telegram talk one another
'''

bot = discord.Client()
bot = commands.Bot(command_prefix = '\\') # command prefix is \

def __init_quote_lang__(lang: str = 'en'):
	try:
		l = db[const.QUOTE_LANG_DB_KEY]
		if(l in wikiquote.supported_languages()):
			return l
		else:
			raise KeyError
	except KeyError:
		db[const.QUOTE_LANG_DB_KEY] = lang
		return lang

@bot.event
async def on_ready():
    print("bot online") #will print "bot online" in the console when the bot is online

@bot.command(help='Simple command which make the bot  respond with "pong!" when you type "\\ping"')
async def ping(ctx):
    await ctx.send("pong!") #simple command so that when you type "\ping" the bot will respond with "pong!"

@bot.command(help='Gives you a quote. Change the language with \\lang command')
async def quote(ctx):
  global quote_lang
  quote = None
  source = None
  while(quote == None and source == None):
    sources = []
    while(sources == []):
      sources = wikiquote.random_titles(lang=quote_lang)
    choices = []
    i = 0
    while(choices == [] and i < len(sources)):
      source = sources[i]
      choices = wikiquote.quotes(source, lang=quote_lang)
      i+=1
    quote = random.choice(choices)
  await ctx.send(f"{quote}\n- {source}")

@bot.command(help='Change language setting for quotes')
async def lang(ctx, new_lang: str = None):
	global quote_lang
	if(new_lang == None):
		await ctx.send(f"No param was given! Language is {quote_lang}")
		return
	try:
		l = new_lang.lower()
		if(l in wikiquote.supported_languages()):
			db[const.QUOTE_LANG_DB_KEY] = l
			quote_lang = l
			await ctx.send(f"Quote Language updated => {quote_lang}")
		else:
			await ctx.send(f"Quote Language '{l}' is not supported. Language is {quote_lang}")
	except:
		await ctx.send("Ops! Something went wrong, how embarassing!🙈")

@bot.command(help = 'Invite the bot to your server')
async def invite(ctx):
	emb = discord.Embed(title = "Invite me", url = discord.utils.oauth_url(bot.user.id, permissions = discord.Permissions(permissions=519232)), colour = discord.Colour.blurple())
	await ctx.send(embed = emb)

'''
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = f"{json_data[0]['q']}\n- {json_data[0]['a']}"
  return(quote)

async def kick(ctx, member : discord.Member):
    try:
        await member.kick(reason=None)
        await ctx.send("kicked "+member.mention) #simple kick command to demonstrate how to get and use member mentions
    except:
        await ctx.send("bot does not have the kick members permission!")

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('!quote'):
    quote = get_quote()
    await message.channel.send(quote)
'''


quote_lang = __init_quote_lang__()


# to keep your bot from shutting down
keep_alive.keep_alive()
bot.run(os.getenv('DISCORD_TOKEN'))
