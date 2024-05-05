import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# URL of the main page with 50 items
headerAddress4ID = "https://www.arabam.com/ikinci-el/otomobil-galeriden?view=Detailed&take=50"

# Code for the user agent required for BeautifulSoup, obtained by inspecting the website.
title = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}


# Function to extract the ID from a string containing the advertisement numbers
def convertString2ID(strLine):
    tokenList = str(strLine).split(">")
    idPart = tokenList[2].split("<")
    id = idPart[0]
    return id


# Function to store an ID if it hasn't been stored before
def storeID(storageList, elementID):
    if (storageList.count(elementID) == 0):
        storageList.append(elementID)
    return storageList


# List to store IDs of advertisements on the main page.
idList = []

# List to store URLs of pages. First 10 pages
pageUrlList = []

# URL to obtain URLs of other pages.
url = "https://www.arabam.com/ikinci-el/otomobil-galeriden?take=50&view=Detailed&page=2"
pageUrlList.append(headerAddress4ID)

# Generating URLs for the first 10 pages
for i in range(2, 11):
    urlTemp = list(url)
    urlTemp.pop()
    urlTemp.append(str(i))
    tempList = map(str, urlTemp)
    returningVariable = ''.join(tempList)
    storeID(pageUrlList, returningVariable)

# Looping through each page URL
for tempIDAddress in pageUrlList:
    detailedPage = requests.get(tempIDAddress, headers=title)
    soup = bs(detailedPage.content, features='lxml')
    noticesID = soup.find_all('p', {'class': 'id'})  # Finding all elements with class 'id'

    # Extracting and storing IDs
    for id in noticesID:
        storeID(idList, convertString2ID(id))

# Converting data to a DataFrame
df = pd.DataFrame(idList, columns=['ID'])

# Writing to an Excel file
excel_path = "galeriden_id.xlsx"
df.to_excel(excel_path, index=False)

print("Data successfully saved to the Excel file.")
