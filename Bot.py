import discord
from discord.ext import commands


client = commands.Bot(command_prefix=".")


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")


@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")


@client.command()
async def ping(ctx):

    await ctx.channel.send(f"Pong {round(client.latency*1000)} ms")



client.run(YOUR TOKEN HERE)
