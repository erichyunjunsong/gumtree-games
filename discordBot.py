# environment variables
import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

# web scraping
import gumtreeScraping as gs

# time delays
import time
import asyncio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))

#should move this to JSON later as a config file
showDescription = True

#Discord bot
#client = discord.Client(intents=discord.Intents.default())
client = commands.Bot(intents=discord.Intents.default(), command_prefix='!')

# @client.command
# async def changeListingDetail(ctx, detailChange: str):
#     ssss

@client.command()
async def toggleDescriptionVisiblity(ctx):
    global showDescription
    showDescription = not showDescription
    await ctx.send(f"Description visibility is set as {showDescription}")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await gumtree_ping()

async def gumtree_ping():
    channel = client.get_channel(CHANNEL_ID)

    while(True):
        for pageNum in range(1,4):
            listings = gs.getListingsOnPage(pageNum)

            for index in range (0, len(listings)):
                if gs.checkIfAd(listings[index]) == False:
                    title = gs.findListingName(listings[index])
                    description = gs.findListingDescription(listings[index])
                    price = gs.findListingPrice(listings[index])
                    location = gs.findListingLocation(listings[index])
                    url = gs.findListingURL(listings[index])
                    image = gs.findListingImage(url)
                    sellerStartYear = gs.findSellerStartYear(url)

                    if (await gs.is_new_listing(title)):
                        await gs.save_listing(title, description, price, location, url, image)
                        if showDescription == True:
                            embed = discord.Embed(
                                title=title,
                                url=url,
                                description=description,
                                color=discord.Color.green()
                            )
                        else: 
                            embed = discord.Embed(
                                title=title,
                                url=url,
                                #description=description,
                                color=discord.Color.green()
                            )

                        embed.add_field(name="Price", value=price)
                        embed.add_field(name="Location", value=location)
                        embed.add_field(name="Seller Start Year", value=sellerStartYear)
                        embed.set_image(url=image)
                        await channel.send(embed=embed)

                time.sleep(5)

        await asyncio.sleep(300)

# Run the Discord bot       
client.run(TOKEN)