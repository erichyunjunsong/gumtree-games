from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import gumtreeListing

# Finding the listing name
def findListingName(listing):
    try:
        listingName = listing.find('span', class_="user-ad-row-new-design__title-span").text
    except:
        listingName = ''
    return listingName

# Finding the description for the listing
def findListingDescription(listing):
    try:
        listingDescription = listing.find('p', class_='user-ad-row-new-design__description-text').text
    except:
        listingDescription = ''
    return listingDescription

# Finding the listing price
def findListingPrice(listing):
    try:
        listingPrice = listing.findNextSibling().find('span', class_='user-ad-price-new-design__price').text
    except:
        listingPrice = ''
    return listingPrice

# Finding the location of the listing
def findListingLocation(listing):
    try:
        listingLocation = listing.findNextSibling().find('div', class_='user-ad-row-new-design__location').text
    except:
        listingLocation = ''
    return listingLocation

# Finding the URL of the listing
def findListingURL(listing):
    try:
        subURL = listing.findParent().attrs['href']
        listingURL = "https://www.gumtree.com.au" + subURL
    except:
        listingURL = ''
    return listingURL


# Checking if the listing is an ad/promoted listing
def checkIfAd(listing):
    try:
        listing.find('span', class_="user-ad-row-new-design__flag-top").text
        return True
    except:
        return False

def findListingInfo(index):
    name = findListingName(listings[index])
    description = findListingDescription(listings[index])
    price = findListingPrice(listings[index])
    location = findListingLocation(listings[index])
    listing = gumtreeListing(name, description, price, location)
    return listing

names = []
descriptions = []
prices = []
locations = []
urls = []

# for pages 1 to 2 
for i in range(1,3):
    url = f'https://www.gumtree.com.au/s-video-games-consoles/page-{i}/c18459r10'
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    listings = soup.find_all('div', class_='user-ad-row-new-design__main-content')

    for index in range (0, len(listings)):
        if checkIfAd(listings[index]) == False:
            names.append(findListingName(listings[index]))
            descriptions.append(findListingDescription(listings[index]))
            prices.append(findListingPrice(listings[index]))
            locations.append(findListingLocation(listings[index]))
            urls.append(findListingURL(listings[index]))

    time.sleep(5)

listingDictionary = dict(name = names, description = descriptions, price = prices, location = locations, url = urls)
df = pd.DataFrame.from_dict(listingDictionary)
df.to_csv('gumtree_videogame_listings.csv', index = False, sep=',') 