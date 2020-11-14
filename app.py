import discord
from discord.ext import commands
from sys import argv

# intents = discord.Intents()
# intents.members = True
token = argv[1]

client = commands.Bot(command_prefix='?')
@client.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, name="Imposteur"))
    await member.send("Coucou et bienvenue sur le serveur EPITA E1.\n Reste respecteux envers les autres, sous peine de te faire bannir. Tu as le rôle @Imposteur par défaut, si il s'agit d'une erreur, contacte un modo")


client.remove_command('help')
client.run(token)