import discord
from discord.ext import commands

client=commands.Bot(command_prefix=".")

@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")



@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")

@client.command()
async def ping(ctx):

    await ctx.channel.send(f"Pong {round(client.latency*1000)} ms")
        
    

@client.command()
async def poll(ctx,*,message):
    emb=discord.Embed(title=" POLL", description=f"{message}")
    msg=await ctx.channel.send(embed=emb)
    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


client.run('YOUR BOT TOKEN')