from random import choice
import nextcord, asyncio, jsonpickle, pymongo
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, Embed
from pymongo import MongoClient

participantes_vip = []
participantes = []

with open('config.json', 'r') as file:
    ret = jsonpickle.decode(file.read())
    p = ret["password"]

cluster = MongoClient(f"mongodb+srv://Zve:{p}@cluster0.lynfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["gambler"]

class Sorteios(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="sorteio", description="Participe do sorteio!", guild_ids=[945348848098893834])
    async def participate(self, i: Interaction, tipo = SlashOption(name="tipo", description="Tipo do sorteio.", choices=["V.I.P.", "Normal"], required=True)):
        global participantes, participantes_vip
        if tipo == "Normal":
            if i.user.id in participantes:
                await i.response.send_message(content="Você já está participando deste sorteio!", ephemeral=True)
                return
            channel = i.guild.get_channel(945348848132427870)
            participantes.append(i.user.id)
            await channel.send(list(participantes))
            await i.response.send_message(content="Registrado com sucesso! Boa sorte!", ephemeral=True)
        else:
            vip = i.guild.get_role(945348848115654694)
            if vip not in i.user.roles:
                await i.response.send_message(content=f"Você precisa ser {vip.mention} para participar desse sorteio!", ephemeral=True)
                return
            if i.user.id in participantes_vip:
                await i.response.send_message(content="Você já está participando deste sorteio!", ephemeral=True)
                return
            channel = i.guild.get_channel(945348848132427871)
            participantes_vip.append(i.user.id)
            await channel.send(str(participantes_vip))
            await i.response.send_message(content=f"Registrado com sucesso! Boa sorte!", ephemeral=True)
    
    @nextcord.slash_command(name="append", description="Só adm pode usar.", guild_ids=[945348848098893834])
    async def append(self, i: Interaction, tipo= SlashOption(name="tipo", description="Tipo do sorteio.", choices=["V.I.P.", "Normal"]),id = SlashOption(name="id", description="id do membro.", required=True)):
        global participantes, participantes_vip
        mod = i.user.get_role(945348848132427866)
        member = i.guild.get_member(int(id))
        if mod not in i.user.roles:
            await i.response.send_message(content=f"Só {mod.mention} pode usar esse comando", ephemeral=True)
            return
        if tipo == "Normal":
            if i.user.id in participantes:
                await i.response.send_message(content="Already Joined", ephemeral=True)
                return
            channel = i.guild.get_channel(945348848132427870)
            participantes.append(member.id)
            await channel.send(list(participantes))
            await i.response.send_message(content="Appended", ephemeral=True)
        else:
            if i.user.id in participantes_vip:
                await i.response.send_message(content="Already Joined", ephemeral=True)
                return
            channel = i.guild.get_channel(945348848132427871)
            participantes_vip.append(member.id)
            await channel.send(str(participantes_vip))
            await i.response.send_message(content=f"Appended", ephemeral=True)
        

    @nextcord.slash_command(name="sortear", description="Só adm pode usar", guild_ids=[945348848098893834])
    async def sortear(self, i: Interaction, tipo = SlashOption(name="tipo", description="Tipo do sorteio.", choices=["V.I.P.", "Normal"], required=True)):
        global participantes, participantes_vip, collection
        if tipo == "Normal":
            winner = i.guild.get_member(choice(participantes))
            await i.response.send_message(content="sorteando...", ephemeral=True)
            embed = Embed(
                type="rich",
                title="**SORTEIO**",
                description=f"Sorteio de **10.000** coins realizado. \n\nO vencedor é: {winner.mention}.",
                color = 0x000000
            )
            ammount = 10000
            participantes.clear()
        else:
            winner = i.guild.get_member(choice(participantes_vip))
            await i.response.send_message(content="sorteando...", ephemeral=True)
            embed = Embed(
                type="rich",
                title="**SORTEIO VIP**",
                description=f"Sorteio de **100.000** coins realizado. \n\nO vencedor é: {winner.mention}.",
                color = 0x000000
            )
            ammount = 100000
            participantes_vip.clear()
        await i.channel.send(content="Sorteando...", delete_after=2)
        await asyncio.sleep(2)
        await i.channel.send(embed=embed)
        count = collection.count_documents({"_id": winner.id})
        if count == 0:
            post = {"_id": winner.id, "saldo": ammount}
            collection.insert_one(post)
            return
        collection.update_one({"_id": winner.id}, {"$inc": {"saldo": ammount}})

def setup(bot):
    bot.add_cog(Sorteios(bot))