import discord
import os
import dotenv
from discord.ext import commands

# Load .env
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv()

# Global variables
OWNER_ID = os.getenv('OWNER_ID')

class Presence(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def presence(self, ctx, presence: discord.Option(str)):
        if int(ctx.user.id) == int(OWNER_ID):
            dotenv.set_key(dotenv_file, "PRESENCE", presence)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=presence))
            await ctx.respond(f"Presence changed to *{presence}*", ephemeral = True)
        else:
            await ctx.respond(f"You don't have permission to use this command.", ephemeral = True)


def setup(bot):
    bot.add_cog(Presence(bot))

