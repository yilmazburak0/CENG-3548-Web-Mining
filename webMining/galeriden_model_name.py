import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# Base URL for the page where we collect the model names of the advertisements
base_url = "https://www.arabam.com/ikinci-el/otomobil-galeriden"

# URL parameter to specify how many advertisements are displayed per page
view_url = "?view=Detailed&take=50"

# User agent code required for BeautifulSoup, obtained by inspecting the website
user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

# Function to find h4 tags with a specific class
def find_h4_with_class(soup, class_name):
    return soup.find_all(lambda tag: tag.name == "h4" and class_name in tag.get("class", []))

# Function to extract model names from a page URL
def extract_model_names(page_url):
    model_names = []
    detailed_page = requests.get(page_url, headers=user_agent)
    soup = bs(detailed_page.content, features='lxml')
    notices_h4 = find_h4_with_class(soup, "model-name")

    # Model names on the main page are not directly available in the URLs of specific cars.
    # Some adjustments are needed.
    for h4 in notices_h4:
        model_name = h4.text.strip().lower()  # Convert to lowercase
        model_name = model_name.replace(" ", "-")  # Replace spaces with "-"
        model_name = model_name.replace(".", "-")  # Replace dots with "-"
        model_name = model_name.replace("--", "-")  # Replace consecutive "--" with single "-"
        while "--" in model_name:  # Loop until there are no consecutive "--"
            model_name = model_name.replace("--", "-")  # Replace consecutive "--" with single "-"
        model_names.append(model_name)
    return model_names

# Function to save data to an Excel file
def save_to_excel(data_list, excel_path):
    # Convert data to a DataFrame
    df = pd.DataFrame(data_list, columns=['Model Name'])

    # Write to an Excel file
    df.to_excel(excel_path, index=False)

    print("Data successfully saved to the Excel file.")

# Main function to orchestrate the process
def main():
    model_names = []  # List to store all model names
    page_url_list = [f"{base_url}{view_url}&page={page}" for page in range(1, 11)]  # Generate URLs for the first 10 pages
    for page_url in page_url_list:
        model_names.extend(extract_model_names(page_url))  # Extract model names from each page and add to the list

    excel_path = "galeriden_model_name.xlsx"
    save_to_excel(model_names, excel_path)  # Save model names to Excel

# Entry point of the script
if __name__ == "__main__":
    main()
