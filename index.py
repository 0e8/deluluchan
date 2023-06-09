# Imports
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Global variables
TOKEN = os.getenv('TOKEN')
OWNER_ID = os.getenv('OWNER_ID')
PRESENCE = os.getenv('PRESENCE')
ACTIVITY = discord.Activity(type=discord.ActivityType.listening, name = PRESENCE)

# Initialize bot
bot = discord.AutoShardedBot(activity = ACTIVITY, debug_guilds=[1089717217618296905])

@bot.event
async def on_ready():
    print(f"[READY] Logged in as {bot.user}")

# Cogs list
cogs_list = [
    'teams',
    'presence'
]

# Load cogs
for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

bot.run(TOKEN)
