import discord
from discord.ext import commands
import tensorflow as tf
import requests
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras import models
g = models.load_model("model.h5")
import os
client = commands.Bot(command_prefix=":)")
@client.event
async def on_ready():
  print("Connected as {}".format(client.user))
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
    m = "Discord bot: https://github.com/arnavg115/discordbot \n Shakespeare api: https://github.com/arnavg115/Shakespeareapi1 \n Shakespeare api docker image: https://hub.docker.com/r/arnavg1q5/shakespeareapi"
    ctx.send(m)
client.run(os.getenv("TOKEN"))
