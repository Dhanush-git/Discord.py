import discord
import my_token
import json
from discord.ext import commands


client = commands.Bot(command_prefix=".",intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")



@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")


@client.command()
async def ping(ctx):

    await ctx.channel.send(f"Pong {round(client.latency*1000)} ms")


@client.command(aliases=['rr'])
async def reactrole(ctx):

    msg =await ctx.fetch_message(792455521793867788)
    print(len(msg.reactions))


        
    await client.wait_for('raw_reaction_add',check= msg.content=="yo")
    print("working")

   

client.run(my_token.secret_token)
