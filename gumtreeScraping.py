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
def findListingPrice(listingAdditionalInfo):
    try:
        listingPrice = listingAdditionalInfo.find('span', class_='user-ad-price-new-design__price').text
    except:
        listingPrice = ''
    return listingPrice

# Finding the location of the listing
def findListingLocation(listingAdditionalInfo):
    try:
        listingLocation = listingAdditionalInfo.find('div', class_='user-ad-row-new-design__location').text
    except:
        listingLocation = ''
    return listingLocation

# Finding the condition of the listing
def findListingCondition(listingAdditionalInfo):
    try:
        listingCondition = listingAdditionalInfo.find('span', class_='user-ad-row-new-design__auto-attribute').text
    except:
        listingCondition = ''
    return listingCondition

def findListingInfo(index):
    name = findListingName(listings[index])
    description = findListingDescription(listings[index])
    price = findListingPrice(listingsAdditionalInfo[index])
    location = findListingLocation(listingsAdditionalInfo[index])
    condition = findListingCondition(listingsAdditionalInfo[index])
    listing = gumtreeListing(name, description, price, location, condition)
    return listing


names = []
descriptions = []
prices = []
locations = []
conditions = []


# for pages 1 to 5 
for i in range(6):
    url = f'https://www.gumtree.com.au/s-video-games-consoles/page-{i}/c18459r10'
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    listings = soup.find_all('div', class_='user-ad-row-new-design__main-content')
    listingsAdditionalInfo = soup.find_all('div', class_='user-ad-row-new-design__right-content')
    
    for index in range (0, len(listings)):
        names.append(findListingName(listings[index]))
        descriptions.append(findListingDescription(listings[index]))
        prices.append(findListingPrice(listingsAdditionalInfo[index]))
        locations.append(findListingLocation(listingsAdditionalInfo[index]))
        conditions.append(findListingCondition(listingsAdditionalInfo[index]))
        #listing = findListingInfo(index)

    time.sleep(5)

listingDictionary = dict(name = names, description = descriptions, price = prices, location = locations, condition = conditions)
df = pd.DataFrame.from_dict(listingDictionary)
df.to_csv('gumtree_videogame_listings.csv', index = False, sep=',') 