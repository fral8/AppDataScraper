import requests
from bs4 import BeautifulSoup
import csv
import re
import datetime

def clean_str(s):
    """Cleans a string by removing non-ASCII characters and line breaks."""
    return re.sub(r'[^\x00-\x7F]+|\n', ' ', s)

def clean_num(s):
    """Cleans a string representing a number by removing commas and non-numeric characters."""
    return re.sub(r'[^\d,.]', '', s)

def get_play_store_data(tag):
    """Scrapes the Play Store for app data based on a given search tag."""
    url = f"https://play.google.com/store/search?q={tag}&c=apps"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all("div", {"class": "Vpfmgd"})
    data = []
    for result in results:
        app_name = clean_str(result.find("div", {"class": "WsMG1c nnK0zc"}).text.strip())
        app_url = "https://play.google.com" + result.find("a")["href"]
        app_response = requests.get(app_url)
        app_soup = BeautifulSoup(app_response.content, "html.parser")
        reviews = app_soup.find_all("div", {"class": "bAhLNe kx8XBd"})
        best_review = ""
        worst_review = ""
        if len(reviews) > 0:
            best_review = clean_str(reviews[0].find("span").text.strip())
            worst_review = clean_str(reviews[-1].find("span").text.strip())
        downloads = clean_num(result.find("div", {"class": "ZFr60d CeoRYc"}).text.strip())
        last_update = clean_str(result.find("div", {"class": "bHi02c"}).text.strip())
        num_apps = clean_num(result.find("div", {"class": "b8cIId ReQCgd Q9MA7b"}).text.strip())
        price = clean_str(result.find("span", {"class": "VfPpfd ZdBevf i5DZme"}).text.strip())
        features = clean_str(result.find("div", {"class": "KoLSrc"}).text.strip())
        data.append([app_name, best_review, worst_review, downloads, last_update, num_apps, price, features])
    return data

def get_app_store_data(tag):
    """Scrapes the App Store for app data based on a given search tag."""
    url = f"https://apps.apple.com/us/search?term={tag}&entity=software"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find_all("div", {"class": "grid3-column"})
    data = []
    for result in results:
        app_name = clean_str(result.find("h3", {"class": "title"}).text.strip())
        app_url = "https://apps.apple.com" + result.find("a")["href"]
        app_response = requests.get(app_url)
        app_soup = BeautifulSoup(app_response.content, "html.parser")
        reviews = app_soup.find_all("div", {"class": "we-customer-review__body"})
        best_review = ""
        worst_review = ""
        if len(reviews) > 0:
            best_review = clean_str(reviews[0].find("p").text.strip())
            worst_review = clean_str(reviews[-1].find("        p").text.strip())
        downloads = clean_num(result.find("span", {"class": "badge badge--product-title"}).text.strip())
        last_update = clean_str(result.find("p", {"class": "whats-new__latest__version"}).text.strip())
        num_apps = ""
        price = clean_str(result.find("span", {"class": "inline-list__item__price"}).text.strip())
        features = clean_str(result.find("ul", {"class": "list"}).text.strip())
        data.append([app_name, best_review, worst_review, downloads, last_update, num_apps, price, features])
    return data
def main():
# Get user input for the tag to search
    tag = input("Enter a tag to search for apps: ")
    # Get data from the Play Store and App Store
    play_store_data = get_play_store_data(tag)
    app_store_data = get_app_store_data(tag)

    # Write data to a CSV file
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{tag}_{now}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["App Name", "Best Review", "Worst Review", "Downloads", "Last Update", "Number of Apps", "Price", "Features"])
        for row in play_store_data:
            writer.writerow(row)
        for row in app_store_data:
            writer.writerow(row)

    print(f"App data written to {filename}")

if __name__ == "__main__":
    main()