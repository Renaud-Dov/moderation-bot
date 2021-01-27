from datetime import datetime, timedelta
from sys import argv

import discord
import json
from discord.ext import commands, tasks

import agenda
from Tools import Data

if __name__ == '__main__':
    token = argv[1]
    intents = discord.Intents.all()
    client = commands.Bot(command_prefix='?t ', intents=intents)

    with open('config.json') as outfile:
        data = json.load(outfile)

    calendar = agenda.Calendar(data["calendarID"], data["link"])


class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot: discord.Client = bot

    @commands.Cog.listener()
    async def on_command_error(self, context, error):
        embed = discord.Embed(title="Error", description=error.args[0], color=discord.Color.red())
        await context.channel.send(embed=embed)

    @commands.command()
    async def StartCalendar(self, context):
        self.SendEventsOfTomorrow.start(context)

    @commands.command()
    async def EndCalendar(self, context):
        self.SendEventsOfTomorrow.cancel()
        embed = discord.Embed(title="Canceled calendar loop", color=discord.Color.green())
        await context.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot ready")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(member)
        await member.add_roles(discord.utils.get(member.guild.roles, id=Data.readGuild(member.guild.id)["role"]))
        await member.send(
            "Coucou et bienvenue sur le serveur EPITA E1.\n "
            "Reste respecteux envers les autres, sous peine de te faire bannir. "
            "Tu as le rôle @Imposteur par défaut, si il s'agit d'une erreur, contacte un modo")

    @commands.command()
    async def change(self, context, role):
        data = Data.readGuild(context.guild.id)
        if len(context.message.role_mentions) == 1:
            data['role'] = context.message.role_mentions[0]
            Data.editGuild(context.guild.id, data)

    @commands.command(aliases=["agenda,calendar"])
    async def Calendar(self, context):
        await self.SendEventsOfTomorrow(context)

    @commands.command()
    async def phrase(self, context, args):
        data = Data.readGuild(context.guild.id)
        data["phrase"] = args
        Data.editGuild(context.guild.id, data)

        embed = discord.Embed(title="Phrase mise à jour", description=args)
        await context.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        Data.createGuild(guild.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        Data.removeGuild(guild.id)

    async def sendEvents(self, context):
        calendar.UpdateCalendar()
        events = calendar.getClassOfTomorrow()

        if events:
            embed = discord.Embed(
                title=f"Résumé de la journée de demain ({(datetime.utcnow() + timedelta(days=1)).strftime('%d/%m/%y')})",
                color=discord.Color.gold())
            for event in events:
                if event.name.startswith("SEMAINE"):
                    embed.description = f"Journée en {event.name.lstrip('SEMAINE EN ').casefold()}"
                else:
                    emoji = Data.GetEmoji(event.name.casefold()) if not None else ''
                    start = event.beginTime.strftime("%Hh%M")
                    end = event.endTime.strftime("%Hh%M")
                    teacher = ' avec {}'.format(event.teacher) if event.teacher != '' else ''

                    embed.add_field(name=f"{emoji}{event.name}{teacher}", value=f"{start} - {end}", inline=False)
            await context.channel.send(embed=embed)

    @tasks.loop(hours=24)
    async def SendEventsOfTomorrow(self, context):
        await self.SendEventsOfTomorrow(context)


client.remove_command('help')
client.add_cog(Bot(client))
client.run(token)
