from bs4 import BeautifulSoup
import requests
import sqlite3
import re

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

# Finding the first image of the listing
def findListingImage(listingURL):
    listing_html_page = requests.get(listingURL)
    soup = BeautifulSoup(listing_html_page.content, 'html.parser')
    listingImageURL = soup.find('meta', {"property":"og:image"})['content']
    return listingImageURL

# Checking if the listing is an ad/promoted listing
def checkIfAd(listing):
    try:
        listing.find('span', class_="user-ad-row-new-design__flag-top").text
        return True
    except:
        return False
    
# Checking if the seller of the listing has any points of concern
def findSellerStartYear(listingURL):
    listing_html_page = requests.get(listingURL)
    soup = BeautifulSoup(listing_html_page.content, 'html.parser')
    subURL = soup.find('a', class_="seller-profile").attrs['href']
    sellerURL = "https://www.gumtree.com.au" + subURL
    seller_html_page = requests.get(sellerURL)
    soup = BeautifulSoup(seller_html_page.content, 'html.parser')
    sellerDetails = soup.find('div', class_="user-rating seller-profile__user-rating-badge").attrs['data-user-rating']
    regexMatch = re.search(r"sellerMemberSinceYear: '(\d{4})'", sellerDetails)
    if regexMatch:
        sellerStartYear = regexMatch.group(1)  # The year will be captured in the first capturing group.
        return sellerStartYear
    else:
        return "Year not found."
    
# Get and return listings for a specific page number of a Gumtree search
def getListingsOnPage(pageNum):
    url = f'https://www.gumtree.com.au/s-video-games-consoles/page-{pageNum}/c18459r10'
    html_page = requests.get(url)
    soup = BeautifulSoup(html_page.content, 'html.parser')
    listings = soup.find_all('div', class_='user-ad-row-new-design__main-content')
    return listings

async def is_new_listing(title):
    #catch instance where the database doesn't exist
    try: 
        conn = sqlite3.connect('listings.db')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Check if the title exists in the database
        cursor.execute('SELECT title FROM listings WHERE title = ?', (title,))
        existing_title = cursor.fetchone()

        # Close the connection
        conn.close()

        # Return True if the title doesn't exist in the database (new listing)
        return not existing_title
    except:
        return True

async def save_listing(title, description, price, location, url, image):
    # Connect to the SQLite database
    conn = sqlite3.connect('listings.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            price NUMBER, 
            location TEXT,
            url TEXT,
            image TEXT
        )
    ''')

    # Insert the new listing into the table
    cursor.execute('INSERT INTO listings (title, description, price, location, url, image) VALUES (?, ?, ?, ?, ?, ?)', (title, description, price, location, url, image,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()