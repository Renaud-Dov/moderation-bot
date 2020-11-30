import discord,json,os
from discord.ext import commands
from sys import argv
import random

token = argv[1]
intents=discord.Intents.all()
client = commands.Bot(command_prefix='?',intents=intents)

@client.event
async def on_member_join(member):
    print(member)
    await member.add_roles(discord.utils.get(member.guild.roles, id=readGuild(member.guild.id)["role"]))
    await member.send("Coucou et bienvenue sur le serveur EPITA E1.\n Reste respecteux envers les autres, sous peine de te faire bannir. Tu as le rôle @Imposteur par défaut, si il s'agit d'une erreur, contacte un modo")

def name(member):
    if member.nick is not None:
        return member.nick
    else:
        return member.name

def convert(role: str,user=False):
    try:
        if not user:
            return int(role.replace(" ", "").lstrip("<@&").rstrip(">"))
        else:
            return int(role.replace(" ", "").lstrip("<@!").rstrip(">"))
    except Exception as e:
        print(e)
        return None

@client.command()
async def change(context,role):
    data=readGuild(context.guild.id)
    data['role']=convert(role)
    editGuild(context.guild.id, data)
    
@client.command()
async def phrase(context,*args):
    data=readGuild(context.guild.id)
    data["phrase"]=" ".join(args)
    editGuild(context.guild.id, data)


@client.event
async def on_guild_join(guild):
    createGuild(guild.id)


@client.event
async def on_guild_remove(guild):
    removeGuild(guild.id)

def createGuild(guildID):
    with open("database/{}.json".format(guildID), "x") as outfile:
        json.dump({"role":0}, outfile)


def removeGuild(guildID):
    os.remove("database/{}.json".format(guildID))


def editGuild(guildID, data):
    with open("database/{}.json".format(guildID), "w") as outfile:
        json.dump(data, outfile)


@client.command()
async def cadeau(context, *args):
    cadeau=list()
    for i in args:
        cadeau.append(i)
    random.shuffle(cadeau)
    message=""
    eucadeau=list()
    for member in cadeau:
        while True:
            a=random.choice(cadeau)
            if a not in eucadeau and a!=member:
                eucadeau.append(a)
                break

        
        await context.guild.get_member(convert(member,True)).send("Tu dois offrir un cadeau à **{}**".format(name(context.guild.get_member(convert(a,True)))))
        message+="\n **{}** offre un cadeau à **{}**".format(name(context.guild.get_member(convert(member,True))),name(context.guild.get_member(convert(a,True))))
    await context.message.channel.send("Messages de Noël envoyés en privé ! 🎅")
    await context.guild.get_member(208480161421721600).send(message)

    print(message)
        

def readGuild(guild):
    with open('database/{}.json'.format(guild), 'r') as outfile:
        return json.load(outfile)

client.remove_command('help')
client.run(token)
client.add_command(cadeau)