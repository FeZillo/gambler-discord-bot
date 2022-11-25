from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord, requests, pymongo, jsonpickle
import funcao.functions as f
from pymongo import MongoClient

with open('config.json', 'r') as file:
    ret = jsonpickle.decode(file.read())
    p = ret["password"]

cluster = MongoClient(f"mongodb+srv://Zve:{p}@cluster0.lynfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

cluster = MongoClient("mongodb+srv://Zve:xdsnuUHHmxOMgf8F@cluster0.lynfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["gambler"]

api = 'https://submundu.neodouglas.repl.co/api/withdraw'
lim = 500000

class Withdraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="withdraw", description="Colete suas Moedas!", guild_ids=[945348848098893834])
    async def withdraw(self, i: Interaction, member: str = SlashOption(name='link', description="Digite o link do perfil com VIP", required=True),
    coins: int = SlashOption(name='coins', description='Quantas coins deseja coletar.', required=True)):
        global collection, lim, api
        if member == None:
            await i.response.send_message(content=f"É necessario inserir um link de perfil com VIP de 500 Moedas!", ephemeral=True)
            return
        conta = collection.find_one({"_id": i.user.id})
        if conta["saldo"] < coins:
            await i.response.send_message(content="Você não tem saldo suficiente para sacar!", ephemeral=True)
            return
        if coins > lim:
            await i.response.send_message(content=f"O limite de hoje é: {f.formata(lim)} coins.")
            return
        await i.response.send_message(content='Coletando...', delete_after=10)
        b = requests.get(f'{api}?link={member}&coins={coins}')
        await i.followup.send(content=f"`{b.text}`", ephemeral=True)
        collection.update_one({"_id": i.user.id}, {"$inc": {"saldo": -coins}})
        lim -= coins

    @commands.command(name='reset')
    @commands.has_role('Mod')
    async def reset(self, ctx):
        global lim
        lim = 500000


def setup(bot):
    bot.add_cog(Withdraw(bot))