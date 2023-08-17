import requests
from bs4 import BeautifulSoup
import pandas as pd
import openai

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


def extract_name_from_text(text):
    openai.api_key = "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"

    messages = [
        {"role": "user", "content": text },
        {"role": "assistant", "content": "Extract the name of the movie or game and nothing else."}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
        max_tokens=50
    )
    return response.choices[0].message['content'].strip()


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
max_requests = 10

# Create a for loop to fill mydata
for j in scraped_data.find_all("tr")[1:]:
    if max_requests <= 0:
        break  # Stop if max requests limit is reached

    row_data = j.find_all("td")
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row

    # Extract name from the "Name" value and assign it back to the DataFrame
    extracted_name = extract_name_from_text(row[headers.index("Name")])
    mydata.at[length, 'Name'] = extracted_name

    max_requests -= 1  # Decrement the remaining requests count

# Export to csv
mydata.to_csv("tpb.csv", index=False)


