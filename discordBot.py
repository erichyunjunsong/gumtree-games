# environment variables
import os
from dotenv import load_dotenv

import discord

# web scraping
import gumtreeScraping as gs
from bs4 import BeautifulSoup
import requests

# time delays
import time
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await gumtree_ping()

@client.event 
async def on_message(message):
    if message.content.startswith('!listings'):
        await check_for_new_listings()

async def check_for_new_listings():
    channel = client.get_channel(CHANNEL_ID)
    for pageNum in range(1,4):
        url = f'https://www.gumtree.com.au/s-video-games-consoles/page-{pageNum}/c18459r10'
        html_page = requests.get(url)
        soup = BeautifulSoup(html_page.content, 'html.parser')
        listings = soup.find_all('div', class_='user-ad-row-new-design__main-content')

        for listingIndex in range (0, len(listings)):
            if gs.checkIfAd(listings[listingIndex]) == False:
                title = gs.findListingName(listings[listingIndex])
                description = gs.findListingDescription(listings[listingIndex])
                price = gs.findListingPrice(listings[listingIndex])
                location = gs.findListingLocation(listings[listingIndex])
                url = gs.findListingURL(listings[listingIndex])
                
                if (await gs.is_new_listing(title)):
                    await gs.save_listing(title, description, price, location, url)

                    embed = discord.Embed(
                        title=title,
                        url=url,
                        description=description,
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Price", value=price)
                    embed.add_field(name="Location", value=location)
                    await channel.send(embed=embed)

        time.sleep(5)

async def gumtree_ping():
    channel = client.get_channel(CHANNEL_ID)

    while(True):
        for i in range(1,4):
            url = f'https://www.gumtree.com.au/s-video-games-consoles/page-{i}/c18459r10'
            html_page = requests.get(url)
            soup = BeautifulSoup(html_page.content, 'html.parser')
            listings = soup.find_all('div', class_='user-ad-row-new-design__main-content')

            for index in range (0, len(listings)):
                if gs.checkIfAd(listings[index]) == False:
                    title = gs.findListingName(listings[index])
                    description = gs.findListingDescription(listings[index])
                    price = gs.findListingPrice(listings[index])
                    location = gs.findListingLocation(listings[index])
                    url = gs.findListingURL(listings[index])
                    
                    if (await gs.is_new_listing(title)):
                        await gs.save_listing(title, description, price, location, url)

                        embed = discord.Embed(
                        title=title,
                        url=url,
                        description=description,
                        color=discord.Color.green()
                        )
                        embed.add_field(name="Price", value=price)
                        embed.add_field(name="Location", value=location)
                        await channel.send(embed=embed)

            time.sleep(5)
        await asyncio.sleep(300)
       
client.run(TOKEN)