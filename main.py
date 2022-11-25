from nextcord.ext import commands
from os import listdir as ld
import nextcord, jsonpickle, os

os.system('pip install pymongo[srv]')

with open('config.json', 'r') as file:
    ret = jsonpickle.decode(file.read())
    TOKEN = ret["token"]

intents = nextcord.Intents()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all(), help_command=None)

def load_cogs(bot):
    bot.load_extension("manager")
    for file in ld("commands"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f"commands.{cog}")

if __name__ == '__main__':
    load_cogs(bot)
    bot.run(TOKEN)
