# Finding the listing name
def findListingName(soup):
    listingNames = []
    divs = soup.find_all('div', class_='user-ad-row-new-design__main-content')
    for items in divs:
        try:
            listingName = items.find('span', class_="user-ad-row-new-design__title-span").text
        except:
            listingName = ''
        listingNames.append(listingName)
    return listingNames

# Finding the description for the listing
def findListingDescription(soup):
    listingDescriptions = []
    divs = soup.find_all('div', class_='user-ad-row-new-design__main-content')
    for items in divs:
        try:
            listingDescription = items.find('p', class_='user-ad-row-new-design__description-text').text
        except:
            listingDescription = ''
        listingDescriptions.append(listingDescription)
    return listingDescriptions

# Finding the listing price
def findListingPrice(soup):
    listingPrices = []
    divs_right = soup.find_all('div', class_='user-ad-row-new-design__right-content')
    for items in divs_right:
        try:
            listingPrice = items.find('span', class_='user-ad-price-new-design__price').text
        except:
            listingPrice = ''
        listingPrices.append(listingPrice)
    return listingPrices

# Finding the location of the listing
def findListingLocation(soup):
    listingLocations = []
    divs_right = soup.find_all('div', class_='user-ad-row-new-design__right-content')
    for items in divs_right:
        try:
            listingLocation = items.find('div', class_='user-ad-row-new-design__location').text
        except:
            listingLocation = ''
        listingLocations.append(listingLocation)
    return listingLocations

# Finding the condition of the listing
def findListingCondition(soup):
    listingConditions = []
    divs_right = soup.find_all('div', class_='user-ad-row-new-design__right-content')
    for items in divs_right:
        try:
            listingCondition = items.find('span', class_='user-ad-row-new-design__auto-attribute').text
        except:
            listingCondition = ''
        listingConditions.append(listingCondition)
    return listingConditions

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import time 

names = []
descriptions = []
prices = []
locations = []
conditions = []

for i in range(6):
    url = f'https://www.gumtree.com.au/s-video-games-consoles/page-{i}/c18459r10'
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    listingName = findListingName(soup)
    listingDescription = findListingDescription(soup)
    listingPrice = findListingPrice(soup)
    listingLocation = findListingLocation(soup)
    listingCondition = findListingCondition(soup)
    names.extend(listingName)
    descriptions.extend(listingDescription)
    prices.extend(listingPrice)
    locations.extend(listingLocation)
    conditions.extend(listingCondition)
    time.sleep(5)

listingDictionary = dict(name = names, description = descriptions, price = prices, location = locations, condition = conditions)
df = pd.DataFrame.from_dict(listingDictionary)
df.to_csv('gumtree_videogame_listings.csv', index = False, sep=',') 