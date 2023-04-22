# bot.py
import os

import discord
from dotenv import load_dotenv
import subprocess
import pandas as pd

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event 
async def on_message(message):
    if message.content.startswith('!listings'):
        #collecting gumtree listings and write to CSV file
        process = subprocess.Popen(['python', 'gumtreeScraping.py'])

        df = pd.read_csv('gumtree_videogame_listings.csv')
        
        for _, row in df.iterrows():
            embed = discord.Embed(
                title=row['name'],
                url=row['url'],
                description=row['description'],
                color=discord.Color.green()
            )
            embed.add_field(name="Price", value=row['price'])
            embed.add_field(name="Location", value=row['location'])
            await message.channel.send(embed=embed)
       
client.run(TOKEN)