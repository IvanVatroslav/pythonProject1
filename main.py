import requests
from bs4 import BeautifulSoup
import pandas as pd


def web_scraper_table():
    url = "https://thepiratebay10.org/top/201"  # Replace with the URL you want to scrape
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the div element with class="example-class"
        table1 = soup.find("table", {"id": "searchResult"})

        if table1:
            # If the div element is found, extract its text
            return table1
        else:
            print("The specified element was not found on the web page.")
            return None
    else:
        print("Failed to fetch data from the web.")
        return None



# Test the web scraper function
scraped_data = web_scraper_table()

# Obtain every title of columns with tag <th>
headers = []

for i in scraped_data.find("tr", {"class": "header"}):
    if i.text != "\n" and "Name" not in i.text:
        headers.append(i.text)
    elif "Name" in i.text:
        headers.append("Name")

mydata = pd.DataFrame(columns = headers)

# Create a for loop to fill mydata
for j in scraped_data.find_all("tr")[1:]:
    row_data = j.find_all("td")
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row

# Export to csv
mydata.to_csv("tpb.csv", index=False)
# Try to read csv
mydata2 = pd.read_csv("tpb.csv")