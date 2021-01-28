import discord
from discord.ext import commands

import giphy_client
from giphy_client.rest import ApiException
import random



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


@client.command()
async def gif(ctx,*,q="random"):

    api_key="Fqi6cJfMpTPkePMA34e6sL4Y39otSJl9"
    api_instance = giphy_client.DefaultApi()

    try: 
    # Search Endpoint
        
        api_response = api_instance.gifs_search_get(api_key, q, limit=5, rating='g')
        lst = list(api_response.data)
        giff = random.choice(lst)

        emb = discord.Embed(title=q)
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')

        await ctx.channel.send(embed=emb)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)
   

client.run('secret_token')
