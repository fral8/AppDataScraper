# AppDataScraper

This is a Python script that scrapes data from the Android Play Store and Apple App Store for apps based on a user-specified tag, and writes the data to a CSV file.

## Usage

To use this script, simply run `python app_scraper.py` from the command line. You'll be prompted to enter a tag to search for apps. Once you enter the tag, the script will scrape both the Play Store and App Store for app data, clean the data, and write it to a CSV file with a name based on the tag and the current date and time.

## Requirements

This script requires Python 3.x and the following Python packages:
- requests
- beautifulsoup4
- pandas

You can install these packages using pip by running `pip install -r requirements.txt` from the command line.

## License

This script is released under the MIT License. See LICENSE for details.
