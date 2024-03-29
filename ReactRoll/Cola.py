import discord
import json
from discord.ext import commands


client = commands.Bot(command_prefix=".",intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"we have logged in as {client.user}")

@client.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == payload.message_id:  # checks if the found member id is equal to the id from the
                                                           # message where a reaction was added
                    if x['emoji'] == payload.emoji.name:  # checks if the found emoji is equal to the reacted emoji
                        role = discord.utils.get(client.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@client.event
async def on_raw_reaction_remove(payload):

    with open('reactrole.json') as react_file:
        data = json.load(react_file)
        for x in data:

            if x['message_id'] == payload.message_id:  # checks if the found member id is equal to the id from the
                                                        # message where a reaction was added
                if x['emoji'] == payload.emoji.name:  # checks if the found emoji is equal to the reacted emoji
                    role = discord.utils.get(client.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                
                await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)
                    


@client.command()
async def hello(ctx):
    await ctx.channel.send(f"Hello! {ctx.author.mention}")


@client.command()
@commands.has_permissions(administrator=True, manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message):

    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open('reactrole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name, 
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open('reactrole.json', 'w') as f:
        json.dump(data, f, indent=4)

client.run('secret_token')
