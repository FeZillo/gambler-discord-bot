from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord, jsonpickle
import funcao.functions as f
import pymongo
from pymongo import MongoClient

with open('config.json', 'r') as file:
    ret = jsonpickle.decode(file.read())
    p = ret["password"]

cluster = MongoClient(f"mongodb+srv://Zve:{p}@cluster0.lynfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["gambler"]

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="saldo", description="verifica seu saldo", guild_ids=[945348848098893834])
    async def saldo(self, i: Interaction, member: nextcord.Member = SlashOption(name='user', description="O usuário que deseja ver o saldo!", required=False)):
        global collection
        if member == None:
            id = i.user.id
        else:
            id = member.id
        count = collection.count_documents({"_id": id})
        if count == 0:
            post = {"_id": id, "saldo": 0}
        conta = collection.find_one({"_id": id})
        await i.response.send_message(content=f"Seu saldo é de: {f.formata(conta['saldo'])}", ephemeral=True)


def setup(bot):
    bot.add_cog(Info(bot))