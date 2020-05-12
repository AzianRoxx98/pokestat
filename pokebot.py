# bot.py
import psycopg2 as SQL
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import numpy as np

TOKEN = ""


bot = commands.Bot(command_prefix='$', description='A bot that greets the user back.')

Connection = SQL.connect(host="ec2-18-213-176-229.compute-1.amazonaws.com", port = "5432", dbname = "d51hgj78fje13v", user="uqmhqntlkzypew", password="38c10d4d2c112be1bfe0d714ba20a2a8c553b92797323e7fbe27fae762e56424")
Cursor = Connection.cursor()
print("Heroku PostgreSQL Connection Successful")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def pstat(ctx, pokemon):
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

@bot.command()
async def pComp(ctx, pokemonOne, pokemonTwo):
    columns = ['ID', 'Name', 'Type 1', 'Type 2', 'Total', 'HP', 'Attack', 'Defense', 'Sp.Atk', 'Sp.Def', 'Speed', 'Generation', 'Legendary']
    header = columns[5:10]
    pokeSQLOne = "SELECT * FROM POKEMON WHERE NAME = '{}';".format(pokemonOne)
    Cursor.execute(pokeSQLOne)
    datOne = Cursor.fetchone()
    datOneList = datOne[5:10]
    print(datOne)
    pokeSQLTwo = "SELECT * FROM POKEMON WHERE NAME = '{}';".format(pokemonTwo)
    Cursor.execute(pokeSQLTwo)
    datTwo = Cursor.fetchone()
    datTwoList = datTwo[5:10]
    print(datTwo)
    print(len(datOneList), len(datTwoList))
    N = 5
    width = 0.35
    fig, ax = plt.subplots()
    index = np.arange(N)
    pokeOne = plt.bar(index, datOneList, width, label = pokemonOne)
    pokeTwo = plt.bar(index + width, datTwoList, width, label = pokemonTwo)
    plt.title(pokemonOne + " vs. " + pokemonTwo)
    plt.xticks(index + width, header)
    plt.legend()
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')
    autolabel(pokeOne)
    autolabel(pokeTwo)
    plt.savefig('compare.png')
    plt.close()
    File = discord.File('compare.png', filename='compare.png')
    await ctx.channel.send(file=File)

bot.run('TOKEN')