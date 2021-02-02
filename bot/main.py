import discord
import tensorflow as tf
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from tensorflow.keras import models
g = models.load_model("facegan/model.h5")
import os
TOKEN = os.getenv(TOKEN)
client = discord.Client()
@client.event
async def on_ready():
  print("Connected as {}".format(client.user))
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(':)face'):
        noise = tf.random.normal([1, 100])
        generated_image = g(noise, training=False)
        img = generated_image[0, :, :, 0].numpy()
        plt.imsave('filename.png', img,cmap = "gray")
        image = Image.open('filename.png')
        new_image = image.resize((400, 400))
        new_image.save('filename.png')
        with open('filename.png', 'rb') as f:
            picture = discord.File(f)
            await message.channel.send(file = picture)

    if message.content.startswith(':)ace'):
        await message.channel.send("Helo!")

client.run(TOKEN)
