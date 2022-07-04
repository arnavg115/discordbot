import discord
from discord.ext import commands
import tensorflow as tf
import requests
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras import models
import os
import random
import asyncio
import csv

fields = []
rows = []
with open("finished.csv","r") as file:
    r = csv.reader(file)
    fields = next(r)
    for row in r:
        rows.append(row)




g = models.load_model("model.h5")
client = commands.Bot(command_prefix=":)")
discord.Intents.reactions = True

@client.event
async def on_ready():
  print("Connected as {}".format(client.user))



@client.command()
async def cudai(ctx,help="Type :)cudai to genrate a question. The command stands for Can yoU Detect an AI. The ai will generate an ending to a sentence. The users must react to the message with which response they think was ai generated within 5 seconds. All of the questions were from a corpus of Jane Austen text. For those curious the model used was t5. Also responses were pregenerated since I don't have enough money for a paid heroku account :( ."):
    rand = random.choice(rows)
    # print(rand)
    desc = "```" +rand[2]
    ijs =random.randint(0,1)
    if  ijs == 0:
        desc += f"\nA) {rand[3].replace(' .','.').strip().replace(' ,', ',')}\nB) {rand[4].strip()}```"
    else:
        desc += f"\nA) {rand[4].strip()}\nB) {rand[3].strip().replace(' .','.').replace(' ,',',')}```"
       
    emd = discord.Embed(title="Question",description=desc)

    out = await ctx.send(embed = emd)

    await asyncio.sleep(10)
    mse = await out.channel.fetch_message(out.id)
    print(mse.reactions)
    users = []
    for g in mse.reactions:
        print(g.emoji == '🅱️')
        if ijs == 0 and (g.emoji == '🅱️' or g.emoji == "🇧" ):
            users = [user async for user in g.users()]
        elif ijs == 1 and (g.emoji == '🅰️' or g.emoji == "🇦"):
            users = [user async for user in g.users()]

    desc2 = "```"
    desc2 += "The correct answer was {}".format("🅱️\n" if ijs == 0 else "🅰️\n")
    l = [user.name for user in users]
    if len(l) == 0:
        desc2 += "No one answered correctly.```"
    else:
        desc2+=", ".join(l)+" got the correct answer.```"
    emd2 = discord.Embed(title="Answer", description=desc2)
    await ctx.send(embed=emd2)


            

    
    

@client.command()
async def face(ctx,help ="Type :)face and the program will generate a face and send into the current channel "):
    noise = tf.random.normal([1, 100])
    generated_image = g(noise, training=False)
    img = generated_image[0, :, :, 0].numpy()
    plt.imsave('filename.png', img,cmap = "gray")
    image = Image.open('filename.png')
    new_image = image.resize((400, 400))
    new_image.save('filename.png')
    with open('filename.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.send("tensorflow GAN",file = picture)
    

@client.command(name = "shakespeare", help ="Type :)shakespeare and the number of characters between 0 and 200 to get a shakespeare quote")
async def shakespeare(ctx, number:int):
    numeber = str(number)
    api = requests.get("https://apiapiapi123.azurewebsites.net/api/v1/request/{}".format(numeber))
    if api.status_code != 200:
        await ctx.send("The api is down for now. Please try again later")
    else:
        dic = api.json()
        for key in dic:
            f = dic[key]
        await ctx.send(f)

@client.command(name = "code",help="If you would like to check out the source code behind this bot here are some sources")
async def code(ctx):
    m = "```Discord bot: https://github.com/arnavg115/discordbot\nShakespeare api: https://github.com/arnavg115/Shakespeareapi1\nShakespeare api docker image: https://hub.docker.com/r/arnavg1q5/shakespeareapi\nT5: https://huggingface.co/Gorilla115/t5-austen```"
    await ctx.send(m)
client.run(os.getenv("TOKEN"))
