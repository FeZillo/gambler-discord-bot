from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import nextcord, jsonpickle, pymongo
from random import randint
import funcao.functions as functions
from pymongo import MongoClient

with open('config.json', 'r') as file:
    ret = jsonpickle.decode(file.read())
    p = ret["password"]

cluster = MongoClient(f"mongodb+srv://Zve:{p}@cluster0.lynfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["gambler"]


class RGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="roleta", description="jogue na roleta por chance de ganhar mais coins!", guild_ids=[945348848098893834])
    async def roleta(self, i: Interaction, cor: str = SlashOption(name="cor", description="Que cor da roleta desejas apostar?", choices=["azul", "vermelho", "verde"], required=True), valor: int = SlashOption(name="valor", description="Quantas coins deseja apostar?", required=True)):
        global collection
        number = randint(0, 30)
        par = await functions.par(number)
        participate = collection.count_documents({"_id": i.user.id})
        if participate == 0:
            post = {"_id": i.user.id, "saldo": 0}
            collection.insert_one(post)
        conta = collection.find_one({"_id": i.user.id})
        if conta["saldo"] < valor:
            await i.response.send_message(content=f"Você não tem saldo suficiente! Digite /saldo para verificar seu saldo.", ephemeral=True, delete_after=10)
            return
        collection.update_one({"_id": i.user.id}, {"$inc": {"saldo": -valor}})
        if number == 0:
            if cor == "verde":
                winner = valor * 10
                await i.response.send_message(content=f"Parabéns! Você apostou {functions.formata(valor)} e ganhou {functions.formata(winner)}!")
                collection.update_one({"_id": i.user.id}, {"$inc": {"saldo": winner}})
                return   
        elif par:
            if cor == "vermelho":
                winner = valor * 2
                await i.response.send_message(content=f"Parabéns! Você apostou {functions.formata(valor)} e ganhou {functions.formata(winner)}!")
                collection.update_one({"_id": i.user.id}, {"$inc": {"saldo": winner}})
                return
        else:
            if cor == "azul":
                winner = valor * 2
                await i.response.send_message(content=f"Parabéns! Você apostou {functions.formata(valor)} e ganhou {functions.formata(winner)}!")
                collection.update_one({"_id": i.user.id}, {"$inc": {"saldo": winner}})
                return
        await i.response.send_message(content=f"Você perdeu {functions.formata(valor)} coins...")
    

def setup(bot):
    bot.add_cog(RGames(bot))

        
        