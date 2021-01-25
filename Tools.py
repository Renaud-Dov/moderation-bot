import json
import os


class Data:
    @staticmethod
    def createGuild(guildID):
        with open("database/{}.json".format(guildID), "x") as outfile:
            json.dump({"role": 0}, outfile)

    @staticmethod
    def removeGuild(guildID):
        os.remove("database/{}.json".format(guildID))

    @staticmethod
    def editGuild(guildID, data):
        with open("database/{}.json".format(guildID), "w") as outfile:
            json.dump(data, outfile)

    @staticmethod
    def readGuild(guild):
        with open('database/{}.json'.format(guild), 'r') as outfile:
            return json.load(outfile)

    @staticmethod
    def GetEmoji(cours: str):
        emoji = {"algorithmique": "💽", "mathématiques": "🧮", "japonais": "🏮", "coreen": None,
                 "te": "✍", "electronique": "🔋", "physique": "🍎", "tim": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "programmation": "💽",
                 "cie": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"}
        if cours in emoji:
            return emoji[cours]
        else:
            return None
