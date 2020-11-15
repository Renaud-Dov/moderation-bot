import discord,json,os
from discord.ext import commands
from sys import argv

token = argv[1]
intents=discord.Intents.all()
client = commands.Bot(command_prefix='?',intents=intents)
@client.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, id=readGuild(member.guild.id)["role"]))
    await member.send("Coucou et bienvenue sur le serveur EPITA E1.\n Reste respecteux envers les autres, sous peine de te faire bannir. Tu as le rôle @Imposteur par défaut, si il s'agit d'une erreur, contacte un modo")

def convert(role: str):
    try:
        return int(role.replace(" ", "").lstrip("<@&").rstrip(">"))
    except Exception as e:
        print(e)
        return None

@client.command()
async def change(context,role):
    role=convert(role)
    context.guild
    editGuild(context.guild.id, {'role':role})
    

@client.event
async def on_guild_join(guild):  # readGuild(message.guild.id)
    rolebot = discord.utils.get(guild.roles, name="CheckStudents").id
    createGuild(guild.id, rolebot)


@client.event
async def on_guild_remove(guild):
    removeGuild(guild.id)

def createGuild(guildID, rolebot):
    with open("database/{}.json".format(guildID), "x") as outfile:
        json.dump({"role":rolebot}, outfile)


def removeGuild(guildID):
    os.remove("database/{}.json".format(guildID))


def editGuild(guildID, data):
    with open("database/{}.json".format(guildID), "w") as outfile:
        json.dump(data, outfile)


def readGuild(guild):
    with open('database/{}.json'.format(guild), 'r') as outfile:
        return json.load(outfile)

client.remove_command('help')
client.run(token)