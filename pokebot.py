# bot.py
import psycopg2 as SQL
import discord
from discord.ext import commands
import matplotlib.pyplot as plt


bot = commands.Bot(command_prefix='$', description='A bot that greets the user back.')

Connection = SQL.connect(host="127.0.0.1", port = "5432", database = "pokemonDB", user="postgres", password="Database1234")
Cursor = Connection.cursor()
print("PostgreSQL Connection Successful")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def pokestat(ctx, pokemon):
    sql = "SELECT * FROM POKEMON WHERE NAME = '{}'".format(pokemon)
    Cursor.execute(sql)
    record = Cursor.fetchall()
    data = list()
    for x in record:
        for y in x:
            data.append(y)
    columns = ['ID','Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp.Atk', 'Sp.Def', 'Speed', 'Generation', 'Legendary']
    headers = columns[5:10]
    datStats = data[5:10]
    plt.barh(headers, datStats)
    for index, value in enumerate(datStats):
        plt.text(value, index, str(value))
    plt.title(pokemon + '\'s' + ' stats')
    plt.savefig('stat.png')
    plt.close()
    File = discord.File('stat.png', filename='stat.png')
    await ctx.channel.send(file=File)

bot.run('NzA4ODgyNTc1ODM3NjI2Mzg5.XreVZw.5kjwiV29HywpqAJribIEzGoQ44g')