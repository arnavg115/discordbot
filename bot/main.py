import discord
from discord.ext import commands
import tensorflow as tf
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras import models
g = models.load_model("model.h5")
import os
client = commands.Bot(command_prefix=":)")
textmd = tf.saved_model.load("one_step")
@client.event
async def on_ready():
  print("Connected as {}".format(client.user))
@client.command()
async def gethelp(ctx):
    await ctx.send("hello")
@client.command()
async def face(ctx):
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
@client.command(name = "shakespeare", help ="Type :)shakespeare and the number of characters between 0 and 200 to ")
async def shakespeare(ctx,numebr:int):
    num = numebr
    if num>200 or num<0:
        num = 50
    states = None
    next_char = tf.constant(['ROMEO:'])
    result = [next_char]

    for n in range(num):
        next_char, states = textmd.generate_one_step(next_char, states=states)
        result.append(next_char)

    m = tf.strings.join(result)[0].numpy().decode("utf-8")
    await ctx.send(m)
client.run("ODA2MjA0ODIyNjc1MzkwNTE0.YBmCwA.GcYWfkz3YW8rU2ZXJvUpcM6OqjI")
