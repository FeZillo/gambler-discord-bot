from nextcord.ext import commands, tasks
from nextcord import Interaction, SlashOption
import nextcord, asyncio, jsonpickle
from random import randint
import funcao.functions as f
import pymongo
from pymongo import MongoClient

with open('config.json', 'r') as file:
    ret = jsonpickle.decode(file.read())
    p = ret["password"]

cluster = MongoClient(f"mongodb+srv://Zve:{p}@cluster0.lynfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["gambler"]

class LGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    
    @nextcord.slash_command(name="lineup", description="Jogue lineup!", guild_ids=[945348848098893834])
    async def line(self, i: Interaction, valor: int = SlashOption(name="valor", description="Valor a ser apostado!", required=True)):
        global collection
        check = collection.count_documents({"_id": i.user.id})
        channel = self.bot.get_channel(949666976547082240)
        def checar(msg: nextcord.Message):
            return msg.author.id == i.user.id and msg.channel.id == channel.id
        if check == 0:
            post = {"_id": i.user.id, "saldo": 0}
        conta = collection.find_one({"_id": i.user.id})
        if conta['saldo'] < valor:
            await i.response.send_message(content=f"Você não tem saldo suficiente! Digite /saldo para verificar seu saldo.", ephemeral=True, delete_after=10)
            return
        collection.update_one({"_id": i.user.id}, {"$inc": {"saldo": -valor}})
        await i.response.send_message(f"Apostado {f.formata(valor)} coins com sucesso!")
        multiplicador = 0.4
        msg = await channel.send(multiplicador)
        while True:
            number = randint(0, 5)
            if number == 0:
                await msg.edit(f"fim! Você apostou {f.formata(valor)} coins e perdeu!")
                return
            multiplicador += 0.2
            await msg.edit(f"{multiplicador:.1f}")
            await asyncio.sleep(0.1)
            desejo = await channel.send("Deseja parar? (digite 'p' para parar ou 'c' para continuar)")
            try:
                parar = await self.bot.wait_for('message', check=checar, timeout=10)
                if parar.content.lower() == "parar" or parar.content.lower() == "p" or parar.content.lower() == "s" or parar.content.lower() == "stop":
                    ganhador = round(valor * multiplicador)
                    collection.update_one({"_id": i.user.id}, {"$inc": {"saldo": ganhador}})
                    await desejo.delete()
                    await parar.delete()
                    break
                elif parar.content.lower() == "c" or parar.content.lower() == "continuar":
                    await desejo.delete()
                    await parar.delete()
                    pass
            except asyncio.TimeoutError:
                await desejo.delete()
                pass
            else:
                pass
        await msg.edit(f"Parabéns! Você apostou {f.formata(valor)} e ganhou {f.formata(round(valor * multiplicador))}")

        
def setup(bot):
    bot.add_cog(LGames(bot))