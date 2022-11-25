from nextcord.ext import commands
import pymongo, jsonpickle, nextcord
from pymongo import MongoClient


with open('config.json', 'r') as file:
    ret = jsonpickle.decode(file.read())
    p = ret["password"]

cluster = MongoClient(f"mongodb+srv://Zve:{p}@cluster0.lynfo.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["discord"]
collection = db["gambler"]

class Vip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="daily", aliases=["dc"])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.has_role("V.I.P.")
    async def daily_coins(self, ctx):
        global collection
        check = collection.count_documents({"_id": ctx.author.id})
        if check == 0:
            post = {"_id": ctx.author.id, "saldo": 10000}
            collection.insert_one(post)
        else:
            collection.update_one({"_id": ctx.author.id}, {"$inc": {"saldo": 10000}})
        await ctx.send("Você coletou suas 10.000 coins do dia!")
    
    @commands.command(name="weekly", aliases=["wc"])
    @commands.cooldown(1, 604800, commands.BucketType.user)
    @commands.has_role("V.I.P.")
    async def weekly_coins(self, ctx):
        global collection
        check = collection.count_documents({"_id": ctx.author.id})
        if check == 0:
            post = {"_id": ctx.author.id, "saldo": 100000}
            collection.insert_one(post)
        else:
            collection.update_one({"_id": ctx.author.id}, {"$inc": {"saldo": 100000}})
        await ctx.send("Você coletou suas 100.000 coins da semana!")

def setup(bot):
    bot.add_cog(Vip(bot))