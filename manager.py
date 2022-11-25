from nextcord.ext import commands
import nextcord
from nextcord import Interaction, SlashOption
import funcao.functions as f
from nextcord.ext.commands.errors import CommandNotFound, MissingRole, CommandOnCooldown, CommandInvokeError
import pymongo, jsonpickle
from pymongo import MongoClient

with open('config.json', 'r') as file:
    ret = jsonpickle.decode(file.read())
    p = ret["password"]

cluster = MongoClient(f"mongodb+srv://Zve:{p}@cluster0.lynfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["gambler"]

class Manager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('BOT ON!')
        
    @nextcord.slash_command(name="registrar", description="registrar um usuário no sistema de apostas", guild_ids=[945348848098893834])
    async def registrar(self, i: Interaction, member: nextcord.Member = SlashOption(name="usuario", description="Usuário a ser registrado!", required=True), saldo: int = SlashOption(name="saldo", description="Saldo adicionado.", required=True)):
        global collection
        mod = i.guild.get_role(945348848132427866)
        if mod in i.user.roles:
            post = {"_id": member.id, "saldo": int(saldo)}
            collection.insert_one(post)
            await i.response.send_message(content=f"{member.mention} registrado com sucesso!")
        else:
            await i.response.send_message(content="Você não tem permissão para usar este comando!", ephemeral=True, delete_after=10)

    @nextcord.slash_command(name="add", description="adiciona saldo a um membro", guild_ids=[945348848098893834])
    async def add(self, i:Interaction, member: nextcord.Member = SlashOption(name="usuario", description="Usuário que será adicionado saldo", required=True), valor: int = SlashOption(name="valor", description="Valor a ser adicionado!", required=True)):
        global collection
        mod = i.guild.get_role(945348848132427866)
        count = collection.count_documents({"_id": member.id})
        if count == 0:
            post = {"_id": member.id, "saldo": 0}
            collection.insert_one(post)
        if mod in i.user.roles:
            collection.update_one({"_id": member.id}, {"$inc": {"saldo": valor}})
            await i.response.send_message(content=f"Adicionado {f.formata(valor)} de saldo para {member.mention}!")
        else:
            await i.response.send_message(content="Você não tem permissão para usar este comando!", ephemeral=True, delete_after=10)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send("""O comando digitado não existe... digite '&help' para ver os comandos existentes.""")
        elif isinstance(error, CommandInvokeError):
            await ctx.send(error, delete_after=5)
        elif isinstance(error, CommandOnCooldown):
            if error.retry_after > 60:
                minutes = error.retry_after / 60
                s = error.retry_after % 60
                if minutes > 60:
                    hours = minutes / 60
                    m = minutes % 60
                    if hours > 24:
                        days = hours / 24
                        hours %= 24
                        await ctx.channel.send(f"O comando está em cooldown, tente novamente em **{int(days)} dias e {int(hours)} horas.**")
                    else:
                        await ctx.channel.send(f"O comando está em cooldown, tente novamente em **{int(hours)} horas e {int(m)} minutos.**")
                else:
                    await ctx.channel.send(f"O comando está em cooldown, tente novamente em **{int(minutes)} minutos e {int(s)} segundos.**")
            else:
                await ctx.channel.send(f"O comando está em cooldown, tente novamente em **{error.retry_after:.1f} segundos.**")
        elif isinstance(error, MissingRole):
            await ctx.send("Você não tem permissão para usar esse comando!")

    
def setup(bot):
    bot.add_cog(Manager(bot))