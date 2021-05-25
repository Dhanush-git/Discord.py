import discord
from discord.ext import commands

import sqlite3

con = sqlite3.connect('level.db')
cur = con.cursor()


client = commands.Bot(command_prefix=".",intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author.bot != True:
        try:

            cur.execute(f"SELECT * FROM GUILD_{message.guild.id} WHERE user_id={message.author.id}")
            result = cur.fetchone()

            if result[1]==99:

                await message.channel.send(f"{message.author.mention} advanced to lvl {result[2]+1}")
                cur.execute(f"UPDATE GUILD_{message.guild.id} SET exp=0, lvl={result[2]+1} WHERE user_id={message.author.id}")
                con.commit()
            else:

                cur.execute(f"UPDATE GUILD_{message.guild.id} SET exp={result[1]+1} WHERE user_id={message.author.id}")
                con.commit()

        except sqlite3.OperationalError:

            pass

    await client.process_commands(message)

@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")

@client.command()
async def ping(ctx):
    await ctx.channel.send(f"Pong {round(client.latency*1000)} ms")


@client.command()
async def init(ctx):

    cur.execute(f'''CREATE TABLE IF NOT EXISTS GUILD_{ctx.guild.id} (user_id int NOT NULL, exp int DEFAULT 0, lvl int DEFAULT 0) ''')

    for x in ctx.guild.members:
        if x.bot != True:
            cur.execute(f"INSERT INTO GUILD_{ctx.guild.id} (user_id) VALUES ({x.id})")

    con.commit()

    await ctx.channel.send("Leveling system initiaized")


@client.command()
async def xp(ctx, user: discord.User = None):

    try:

        if user == None :
            cur.execute(f"SELECT * FROM GUILD_{ctx.guild.id} WHERE user_id={ctx.author.id}")
            result = cur.fetchone()

            await ctx.channel.send(f"{ctx.author.mention} Exp: {result[1]} Lvl: {result[2]}")

        else:
             cur.execute(f"SELECT * FROM GUILD_{ctx.guild.id} WHERE user_id={user.id}")
             result = cur.fetchone()

             if result!=None:
                 await ctx.channel.send(f"{user.mention} Exp: {result[1]} Lvl: {result[2]}")
             else:

                 await ctx.channel.send("Hmm no such user in the db")

    except sqlite3.OperationalError:

        await ctx.channel.send("DataBase not initialized")


client.run('YOUR_TOKEN_HERE')
