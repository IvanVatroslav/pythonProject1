import requests
from bs4 import BeautifulSoup

def web_scraper():
    url = "https://thepiratebay10.org/top/201"  # Replace with the URL you want to scrape
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the div element with class="example-class"
        div_element = soup.find("div", {"class": "detName"})

        if div_element:
            # If the div element is found, extract its text
            data = div_element.text
            return data
        else:
            print("The specified element was not found on the web page.")
            return None
    else:
        print("Failed to fetch data from the web.")
        return None

# Test the web scraper function
scraped_data = web_scraper()
if scraped_data:
    print(scraped_data)