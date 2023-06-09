import discord
import asyncio
import random
from datetime import datetime
from discord.ext import commands

class Teams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def teams(self, ctx, number_of_teams: discord.Option(int), size_of_teams: discord.Option(int), joining_time: discord.Option(int)):
        # Variables
        players = []
        cmd_init_player = ctx.user

        # Define embed
        embed = discord.Embed(
            title = "Teams",
            # description = ""
            color = discord.Colour.green()
        )

        embed.set_author(name = ctx.author)

        embed.add_field(name = f"Number of teams: {number_of_teams}", value = "*Number of teams for players to assign to*", inline = True)
        embed.add_field(name = f"Size of teams: {size_of_teams}", value = "*Number of slots in each team*", inline = True)
        embed.add_field(name = f"Time to join: {joining_time}", value = "*Set time to join team draw*", inline = True)

        # Views / Buttons
        class confirmation_view(discord.ui.View): # Confirmation view
            # Confirm button
            @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.success, emoji = "✔️")
            async def confirm_button_callback(self, button, interaction):
                if interaction.user.id == ctx.author.id:
                    class joining_view(discord.ui.View): # Joining view
                        @discord.ui.button(label = "Join", style = discord.ButtonStyle.success, emoji = "✔️")
                        async def join_button_callback(self, button, interaction):
                            if str(interaction.user) in players:
                                await interaction.response.send_message(f"You have already joined!", ephemeral = True)

                            else:
                                players.append(str(interaction.user))
                                await interaction.response.send_message("Joined!", ephemeral = True)

                    embed.fields = [] # Empty embed
                    embed.description = f"Press ***Join*** button to enter.\n*{joining_time} seconds left!*"
                    await self.message.edit(embed = embed, view = joining_view()) # Add joining_view()
                    await interaction.response.defer()

                    # Results script
                    await asyncio.sleep(joining_time / 2)

                    embed.description = f"Press ***Join*** button to enter.\n*{joining_time / 2} seconds left!*"
                    await self.message.edit(embed = embed)
                    await asyncio.sleep(joining_time / 2)

                    await self.message.edit(view = None)
                    
                    # Make squads
                    for team in range(number_of_teams):
                        try:
                            squad = random.sample(players, size_of_teams)
                            str_squad = str(squad).replace("[","").replace("]","").replace(","," ").replace("'","")
                            embed.add_field(name = f"Team {team + 1}", value = str_squad)
                        except: # Not enough players!!!
                            embed.fields= []
                            embed.add_field(name = f"Error!", value = "Not enough players.", inline = False)

                        try:
                            # Delete players (that are already assigned to team) from players array
                            for player in squad:
                                players.remove(player)
                        except:
                            pass

                    embed.description = None
                    await self.message.edit(embed = embed)

                else:
                    await interaction.response.send_message("Only command initiator can do it!", ephemeral = True)

            # Cancel button
            @discord.ui.button(label = "Cancel", style = discord.ButtonStyle.danger, emoji = "➖")
            async def cancel_button_callback(self, button, interaction):
                if interaction.user.id == ctx.author.id:
                    # Tell user that command was canceled successfully
                    embed.title = "Command canceled successfully"
                    embed.fields = [] # Empty embed

                    self.disable_all_items()
                    await self.message.edit(embed = embed, view = self)
                
                    # Delete message after 2.5s
                    await interaction.response.defer()
                    await asyncio.sleep(5)
                    await self.message.delete()
                else:
                    await interaction.response.send_message("Only command initiator can do it!", ephemeral = True)


        # Avoid negative and =0 variables
        if number_of_teams < 1:
            await ctx.respond(f"Too few teams! ({number_of_teams})", ephemeral = True)
            return

        if size_of_teams < 1:
            await ctx.respond(f"Not enough players per team! ({size_of_teams})", ephemeral = True)
            return

        if joining_time < 5:
            await ctx.respond(f"Too small joining time! ({joining_time})", ephemeral = True)
            return
        elif joining_time > 60:
            ctx.respond(f"Too large joining time! ({joining_time})", ephemeral = True)
            return
        
        # Send embed // Disable after 60s inactivity
        await ctx.respond(embed = embed, view = confirmation_view())

def setup(bot):
    bot.add_cog(Teams(bot))
