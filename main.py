import os
import sys
import discord
from keep_alive import keep_alive
import asyncio
import requests
import time
import asyncio
import aiohttp

link = os.environ['LINK']
link = str(link)
mute_role = 'Muted'

async def check_ping():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://hc-ping.com/1cb3ea9d-4a3e-4a84-9305-8f6c2879a60e"
        ) as response:
            if response.status == 60:
                print("Check passed!")
            else:
                print("Check failed!")


async def main():
    while True:
        await check_ping()
        await asyncio.sleep(300)  # wait 5 minutes before pinging again


bots = False
self = os.environ['self']

loop_on = True

guild_id = os.environ['GUILD']
role_name = "bot"
role_to_change = "1033847146279088189"

invite = os.environ['INVITE']


"""Notes: add buttons
fix the responses to ban, mute, kick slash_commands
Fix mute slash_command
add more moderation slash_commands"""
"""To fix slash_slash_commands not an attribute error:
pip uninstall discord.py
pip install discord
pip install pycord
pip install py-cord"""
"""pip install PyNaCl"""

PIN1 = os.environ['pin1']
PIN2 = os.environ['pin2']

bot = discord.Bot()
USER = os.environ['username']


@bot.slash_command(description="test")
async def test(ctx):
    await ctx.respond("This is a test!")


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


@bot.slash_command(description='Help with different slash_commands (INCOMPLETE)')
async def help(ctx):
    embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    embedVar.add_field(name="Help", value="Displays this Embed", inline=False)
    embedVar.add_field(name="Users",
                       value="Sends a list of logged users (Admin slash_command)",
                       inline=False)

    embedVar.add_field(
        name='Mute',
        value=
        'Mute a member to prevent them from chatting (Not Currently Functional)'
    )
    embedVar.add_field(name='Kick', value='Remove a member from the server')
    embedVar.add_field(
        name='Ban',
        value='Ban a member (Requires user to have ban member permission')
    embedVar.add_field(
        name='Unban',
        value=
        'Allows a user to join the server again after being banned (Not Currently Functional)'
    )
    embedVar.add_field(name='Join', value='Join the voice channel you\'re in')
    embedVar.add_field(name='Leave',
                       value='Leave the vc the bot is currently in')
    author = ctx.author
    channel = await author.create_dm()

    await channel.send(author, embed=embedVar)
    await channel.send(
        'Some slash_commands are not currently fuctional, and others will be added in the future'
    )
    await ctx.respond("Message sent to your DMs")


@bot.slash_command(description='Emergency Shutoff')
async def shutoff(ctx, pin, pin2, confirm):
    author = ctx.author
    channel = await author.create_dm()

    if pin == PIN1 and pin2 == PIN2 and confirm.lower().startswith('y'):
        await ctx.respond('Shutting Off')
        await channel.send('Bot Shutoff initiated by {}'.format(ctx.author))
        INCIDENT = ('Shutoff Initiated by {}'.format(ctx.author))
        print('Shutting Off')
        sys.exit
    elif confirm.lower().startswith('n'):
        await ctx.respond('Shutoff Averted')
    else:
        await ctx.respond('Invalid User, Incident Logged')
        INCIDENT = ('Failed Shutoff by {}'.format(ctx.author))
        



@bot.slash_command(name='setstatus', description='Set the various bot statuses')
async def status(ctx, pin, type, status, *, message=None):
    user = ctx.author
    if pin == PIN1 or pin == PIN2:

        pass

    else:
        await ctx.respond('Invalid User {}'.format(user))
        return

    if type.lower() == 'game':
        activity = discord.Game(name=message)
    elif type.lower() == 'streaming':
        activity = discord.Streaming(name=message, url=message)
    elif type.lower() == 'listening':
        activity = discord.Activity(type=discord.ActivityType.listening,
                                    name=message)
    elif type.lower() == 'watching':
        activity = discord.Activity(type=discord.ActivityType.watching,
                                    name="a movie")

    else:
        await ctx.respond('Failed to change status')

    if status.lower() == 'idle':
        await bot.change_presence(status=discord.Status.idle,
                                  activity=activity)
        await ctx.respond('Status Updated')
    elif status.lower() == 'online':
        await bot.change_presence(status=discord.Status.online,
                                  activity=activity)
        await ctx.respond('Status Updated')

    else:
        await ctx.respond('Failed to change status')


@bot.slash_command(name='mute',description='Mute a member')
async def mute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.manage_members:
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not mute_role:
            mute_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(mute_role, send_messages=False)
        await member.add_roles(mute_role)
        await ctx.send(f"{member.mention} has been muted.")
    else:
        await ctx.send("You don't have permission to use this slash_command.")

@bot.slash_command(name='unmute',description='Unmute a member')
async def unmute(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.manage_members:
        mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if mute_role in member.roles:
            await member.remove_roles(mute_role)
            await ctx.send(f"{member.mention} has been unmuted.")
        else:
            await ctx.send(f"{member.mention} is not muted.")
    else:
        await ctx.send("You don't have permission to use this slash_command.")



@bot.slash_command(name='join',
             description='Tells the bot to join the voice channel')
async def join(ctx):
    if not ctx.author.voice:
        await ctx.respond("{} is not connected to a voice channel".format(
            ctx.author.name))
        return
    else:
        channel = ctx.author.voice.channel
    await channel.connect()
    await ctx.respond('Connected')


@bot.slash_command(name='leave', description='Make the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
        await ctx.respond('Left Voice Channel')
    else:
        await ctx.respond("The bot is not connected to a voice channel.")


@bot.slash_command(name='purge')
async def purge(ctx, limit):
    if int(limit) > 1000:
        await ctx.respond('Please use the masspurge slash_command')
        return
    channel = ctx.channel
    await channel.purge(limit=int(limit))
    await ctx.respond('Purged {} messages'.format(str(limit)), delete_after=2)




@bot.slash_command(name='masspurge')
async def masspurge(ctx, pin, confirm, limit):
    if pin == PIN2 and confirm.lower().startswith('y'):
        channel = ctx.channel
        await channel.purge(limit=int(limit))
        await ctx.respond('Purged {} messages'.format(str(limit)),
                          delete_after=2)


@bot.slash_command(name='terminate')
async def terminate(ctx,
                    user: discord.Member,
                    pin,
                    *,
                    reason="No reason provided"):
    if pin == PIN1 or pin == PIN2:
        await user.kick(reason=reason)
    else:
        await ctx.respond('Failed', delete_after=3)
        return




class MyView(discord.ui.View):
    @discord.ui.select(  # the decorator that lets you specify the properties of the select menu
        placeholder=
        "Levels (Test slash_command)",  # the placeholder text that will be displayed if nothing is selected
        min_values=
        1,  # the minimum number of values that must be selected by the users
        max_values=
        1,  # the maximum number of values that can be selected by the users
        options=
        [  # the list of options from which users can choose, a required field
            discord.SelectOption(label="Level 1", description="Low priority"),
            discord.SelectOption(label="Level 2",
                                 description="Non-Urgent, Semi-important"),
            discord.SelectOption(label="Level 3", description="Urgent")
        ])
    async def select_callback(
        self, select, interaction
    ):  # the function called when the user is done selecting options
        if select.values[0] == 'Level 1':
            await interaction.response.send_message(
                'You selected "Low Priority"')
        elif select.values[0] == 'Level 2':
            await interaction.response.send_message(
                'You selected "Non-Urgent/Semi-important"')
        elif select.values[0] == 'Level 3':
            await interaction.response.send_message('You selected "Urgent"')

            await interaction.response.send_message(
                f"Awesome! I like {select.values[0]} too!")


@bot.slash_command(name='send')
async def send(ctx):
    await ctx.respond("Select a level to send this to", view=MyView())

@bot.slash_command(name='test2')
async def testing(ctx):
  await ctx.respond('Tested')
  
#keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
