import discord
from discord.ext import commands,tasks
from restaurant import input_restaurant
from order_file import write_file, read_file
from today_restaurant import write_restaurant_file, read_restaurant_file
import time
import threading

restaurant_data = []
total_order = {}
bot = commands.Bot(command_prefix="/")

today_restaurant = {}



@bot.event
async def on_ready():
    print(">> Bot is online << ")
   # await channel.send('Hello', file=discord.File('cool.png', 'testing.png'))


@bot.event
async def on_member_join(member):
    print(F'{member} join!')
    channel = bot.get_channel(692384983314333719)
    await channel.send(F'{member} join')
    await channel.send('You can type "//help" and then will see all commands.')
    #await channel.send('Hello', file=discord.File('cool.png', 'testing.png'))

@bot.event
async def on_member_remove(member):
    print(F'{member} remove!')
    channel = bot.get_channel(692384983314333719)
    await channel.send(F'{member} leave')

@bot.command()
async def today_eat(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def view(ctx, *arg):
    if(len(arg) == 0):
        for item in restaurant_data:
            await ctx.send(item['name'] + '\n電話: ' + item['tel']
                            + '\n地址: ' + item['address'] +
                            "\n-------------------------------")

    elif(len(arg) == 1):
        for item in restaurant_data:
            if(item['name'] == arg[0]):
                await ctx.send(item['name'] + '\n電話: ' + item['tel']
                            + '\n地址: ' + item['address'] +
                            "\n-------------------------------")
                return
        await ctx.send('cannot find restaurant')
    else:
        ctx.send('error argument!!!!')

@bot.command()
async def order(ctx, *arg):#人 餐 錢
    if(len(arg) == 0):
        await ctx.send('error arugment')
    else:
        author = str(arg[0])
        order = []
        order.append(str(arg[1]))
        order.append(str(arg[2]))
        total_order[author] = order
        write_file(total_order)
        print(total_order)


@bot.command()
async def all_order(ctx):
    output = ''
    for item in total_order:
        output = output + item + " : "
        for i in total_order[item]:
            output = output + i + ' '
        output = output + '\n'
    await ctx.send(output)

@bot.command()
async def finish(ctx):
    output = ''
    print(today_restaurant)
    output = today_restaurant['name'] + '\n電話: ' + today_restaurant['tel'] + '\n地址: ' + today_restaurant['address'] + "\n-------------------------------+\n"
    for item in total_order:
        output = output + item + " : "
        for i in total_order[item]:
            output = output + i + ' '
        output = output + '\n'
    await ctx.send(output)

@bot.command()
async def decide(ctx, *arg):
    global today_restaurant
    if(len(arg) == 1):
        r = str(arg[0])
        for item in restaurant_data:
            if(item['name'] == r):
                today_restaurant = item
        await ctx.send('today restaurant is set')
        await ctx.send(today_restaurant['name'] + '\n電話: ' + today_restaurant['tel']
                            + '\n地址: ' + today_restaurant['address'] +
                            "\n-------------------------------")
        write_restaurant_file(today_restaurant)
    else:
        await ctx.send('error message')

if __name__ == '__main__':

    restaurant_data = input_restaurant()
    total_order = read_file()
    today_restaurant = read_restaurant_file()
    print(today_restaurant)
    bot.run("NjkyMzc5MzM0NDEzMTIzNTg0.XntqyA.vlDzpJSe3hHENz5fGkRH9ScJ9DQ")