import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import numpy as np

# We are now going to visit a specific advertisement page instead of the main page.
# With the data we collected earlier (id, model name, title), we will create a specific URL for each car.
# The URL structure for each car: https://www.arabam.com/ilan/galeriden-satilik-{car_model_name}/{car_title}/{car_id}

# Excel files where the previous data is stored.
excel_files = ["galeriden_model_name.xlsx", "galeriden_title.xlsx", "galeriden_id.xlsx"]

# Convert each Excel file to a DataFrame.
dataframes = [pd.read_excel(file) for file in excel_files]

# Base URL
base_url = "https://www.arabam.com/ilan/galeriden-satilik-"

# Generate URLs and store them in a list
urls = []
for i in range(len(dataframes[0])):
    values = [df.iloc[i, 0] for df in dataframes]
    url = base_url + "/".join(map(str, values))
    urls.append(url)

# Extract data for each URL
extracted_data = []

for url in urls:
    # Send a request to the URL
    response = requests.get(url)

    # If the request is successful, extract the data
    if response.status_code == 200:
        soup = bs(response.content, "html.parser")

        # Get the product price
        product_price = soup.find("div", class_="product-price").text.strip()

        # Extracting the date from different divs based on the class
        # Get the value of js-hook-copy-text from the first property-value div
        first_property_value = soup.find("div", class_="property-value")
        first_property_value_text = first_property_value.find("div", id="js-hook-copy-text").text.strip() if first_property_value else None

        # Get other property values (model, year, brand, etc.)
        property_values = [div.text.strip() for div in soup.find_all("div", class_="property-value")[1:]]

        # Store the extracted data as a tuple
        extracted_data.append((product_price, first_property_value_text, property_values))
    else:
        # Print error if there's an issue with the request
        print(f"Error: {response.status_code} - URL: {url}")

# Column names for the Excel file
column_names = ["Ad No", "Ad Date", "Brand", "Series", "Model", "Year", "Mileage", "Transmission Type",
                "Fuel Type", "Body Type", "Color", "Engine Volume", "Engine Power", "Drive", "Vehicle Condition",
                "Average Fuel Consumption", "Fuel Tank", "Paint-Changed", "Exchangeable", "From Whom"]

# Create an empty list to hold dictionaries for row data
rows = []

# Iterate over extracted data and fill the list of dictionaries
for data in extracted_data:
    # Extract individual data elements
    product_price, first_property_value_text, property_values = data

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
                "Exchangeable": property_values[17], "From Whom": property_values[18]}

    # Append the row data to the list
    rows.append(row_data)

# Create DataFrame from the list of dictionaries
df = pd.DataFrame(rows)

# Save DataFrame to an Excel file
df.to_excel("extracted_data.xlsx", index=False)

print("Excel file created successfully.")