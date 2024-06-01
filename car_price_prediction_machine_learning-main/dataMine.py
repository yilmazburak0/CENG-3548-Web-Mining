import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np

# URL to fetch data from
mainAddress = "https://www.arabam.com/ikinci-el/otomobil?currency=TL&maxPrice=440000&minPrice=410001&take=50&view=Detailed&page=3"
baslik = {'user-agent' : ''}  # Header to mimic a browser user agent
#Some websites may block requests from outside the browser (for example, automated scripts or bots).
# Adding a User-Agent string gives the impression that the request is coming from a real browser and prevents such blocking.

# Array to store URLs of individual ads
urlArr = []

try:
    # Loop through pages 1 to 50 (site has max 50 pages)
    for i in range(1, 50):
        # Split the main URL by '='
        tempURL = mainAddress.split('=')
        # Modify the last part of the URL to the current page number
        tempURL[-1] = str(i)
        # Join the URL parts back into a single string
        currentURL = "=".join(tempURL)
        # Fetch the content of the current page
        page = requests.get(currentURL, headers=baslik)
        # Parse the page content
        soupParser = bs(page.content, 'html.parser')
        # Find all 'a' tags with the specified class to get ad URLs
        a_tags = soupParser.findAll('a', class_='df df-fd h100')
        # Extract the 'href' attribute from each 'a' tag
        urls = [a['href'] for a in a_tags if 'href' in a.attrs]
        # Append the full URL of each ad to the urlArr
        for url in urls:
            urlArr.append(f"https://www.arabam.com{url}")

except Exception as e:
    print(f"An error occurred while fetching URLs: {e}")

# List to store extracted data
extracted_data = []

# Loop through each ad URL
for url in urlArr:
    try:
        # Send a request to the URL
        response = requests.get(url)

        # If the request is successful, extract the data
        if response.status_code == 200:
            soup = bs(response.content, "html.parser")

            # Get the product price, if it exists
            product_price_element = soup.find("div", class_="product-price")
            product_price = product_price_element.text.strip() if product_price_element else None

            # Get the value of js-hook-copy-text from the first property-value div
            first_property_value = soup.find("div", class_="property-value")
            first_property_value_text = first_property_value.find("div", id="js-hook-copy-text").text.strip() if first_property_value else None

            # Get other property values (model, year, brand, etc.)
            property_values = [div.text.strip() for div in soup.find_all("div", class_="property-value")[1:]]

            # Store the extracted data as a tuple
            extracted_data.append((first_property_value_text, property_values, product_price))
        else:
            # Print error if there's an issue with the request
            print(f"Error: {response.status_code} - URL: {url}")
    except Exception as e:
        print(f"An error occurred while processing URL {url}: {e}")
    # Optional: Sleep to avoid overwhelming the server
    # time.sleep(1)

# Column names for the Excel file
column_names = ["Ad No", "Ad Date", "Brand", "Series", "Model", "Year", "Mileage", "Transmission Type",
                "Fuel Type", "Body Type", "Color", "Engine Volume", "Engine Power", "Drive", "Vehicle Condition",
                "Average Fuel Consumption", "Fuel Tank", "Paint-Changed", "Exchangeable", "From Whom", "Price"]

# Create an empty list to hold dictionaries for row data
rows = []

# Iterate over extracted data and fill the list of dictionaries
for data in extracted_data:
    try:
        # Extract individual data elements
        first_property_value_text, property_values, product_price = data

        # Fill with NaN if property_values is not long enough
        while len(property_values) < len(column_names):
            property_values.append(np.nan)

        # Create a dictionary to hold the row data
        row_data = {"Ad No": first_property_value_text, "Ad Date": property_values[0],
                    "Brand": property_values[1], "Series": property_values[2], "Model": property_values[3],
                    "Year": property_values[4], "Mileage": property_values[5], "Transmission Type": property_values[6],
                    "Fuel Type": property_values[7], "Body Type": property_values[8], "Color": property_values[9],
                    "Engine Volume": property_values[10], "Engine Power": property_values[11], "Drive": property_values[12],
                    "Vehicle Condition": property_values[13], "Average Fuel Consumption": property_values[14],
                    "Fuel Tank": property_values[15], "Paint-Changed": property_values[16],
                    "Exchangeable": property_values[17], "From Whom": property_values[18], "Price": product_price}

        # Append the row data to the list
        rows.append(row_data)
    except Exception as e:
        print(f"An error occurred while processing extracted data: {e}")

# Create DataFrame from the list of dictionaries
df = pd.DataFrame(rows)

try:
    # Save DataFrame to an Excel file
    df.to_excel("../Csv_Excel_files/extracted_data_41_44.xlsx", index=False)
    print("Excel file created successfully.")
except Exception as e:
    print(f"An error occurred while saving to Excel: {e}")
