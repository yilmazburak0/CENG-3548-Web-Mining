import requests
from bs4 import BeautifulSoup as bs
import string
import pandas as pd

base_url = "https://www.arabam.com/ikinci-el/otomobil-galeriden"  # Base URL of the page where we collect the titles of the advertisements
view_url = "?view=Detailed&take=50"  # Parameter to specify how many advertisements are displayed per page
user_agent = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}  # User agent code required for BeautifulSoup, obtained by inspecting the website


# Function to find p tags with a specific class
def find_p_with_class(soup, class_name):
    return soup.find_all(lambda tag: tag.name == "p" and class_name in tag.get("class", []))


# Function to extract titles from a page URL
def extract_title(page_url):
    titles = []  # List to store titles of cars on a specific page
    detailed_page = requests.get(page_url,
                                 headers=user_agent)  # Make a request to the URL where car advertisements are listed
    soup = bs(detailed_page.content, features='lxml')
    notices_p = find_p_with_class(soup, "title")  # Title of the car is stored in a p tag with class "title"

    # Titles obtained from the main page are not directly available in the URLs of specific cars. Some adjustments are needed.

    # Replace all special characters with '-'
    translator = str.maketrans(string.punctuation.replace("_", "") + '“',
                               '-' * (len(string.punctuation.replace("_", "")) + 1))

    for p in notices_p:
        title = p.text.strip().lower()  # Convert to lowercase
        title = title.replace(" ", "-")  # Replace spaces with "-"
        title = title.replace(".", "-")  # Replace dots with "-"
        title = title.replace("ç", "c")  # Replace 'ç' with 'c'
        title = title.replace("ğ", "g")  # Replace 'ğ' with 'g'
        title = title.replace("ö", "o")  # Replace 'ö' with 'o'
        title = title.replace("ş", "s")  # Replace 'ş' with 's'
        title = title.replace("ı", "i")  # Replace 'ı' with 'i'
        title = title.replace("ü", "u")  # Replace 'ü' with 'u'

        title = title.translate(translator)  # Replace all special characters with '-'
        title = title.replace("_", "")  # Remove "_" characters
        title = title.replace("’", "")  # Remove "’" characters
        title = title.replace('”', '-')  # Replace double quotes with '-'

        title = title.strip("-")  # Remove leading and trailing '-' characters
        title = title.replace("--", "-")  # Replace consecutive "--" with single "-"
        while "--" in title:  # Loop until there are no consecutive "--"
            title = title.replace("--", "-")  # Replace consecutive "--" with single "-"

        if "arabam-com" not in title:  # Some p tags with class "title" do not contain car titles, but include "arabam-com" string. Remove those from the list.
            titles.append(title)

    return titles


# Function to save titles to an Excel file
def save_to_excel(data_list, excel_path):
    # Convert data to a DataFrame
    df = pd.DataFrame(data_list, columns=['Title'])

    # Write to an Excel file
    df.to_excel(excel_path, index=False)

    print("Data successfully saved to the Excel file.")


#Main function for organising the process
def main():
    galeriden_titles = []  # List to store all titles of cars on main pages
    page_url_list = [f"{base_url}{view_url}&page={page}" for page in
                     range(1, 11)]  # Generate URLs for the first 10 pages
    for page_url in page_url_list:
        galeriden_titles.extend(extract_title(page_url))  # Extract titles from each page and add to the list

    excel_path = "galeriden_title.xlsx"
    save_to_excel(galeriden_titles, excel_path)  # Save titles to Excel


# Entry point of the script
if __name__ == "__main__":
    main()
