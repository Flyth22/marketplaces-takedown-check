from title_scrape_functions import excel_to_pandas
from title_scrape_functions import excel_from_dataframe
from bs4 import BeautifulSoup
import pandas as pd
import requests
import openpyxl
import os

pd.options.mode.chained_assignment = None  # default='warn'

pd_listings_report = excel_to_pandas()

# headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}


def extract_title(pdframe):
    url = pdframe['URL']
    a = pdframe.name
    og_url = "not found"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, features="html.parser")
        og_url = response.url
        title = soup.find("title").text
    except AttributeError:
        title = "Check Manually: attribute error"
    except requests.exceptions.ReadTimeout as err:
        title = err
    except requests.exceptions.ConnectionError:
        title = "Check Manually: connection error"
    pdframe['URL_TITLE'] = title
    pdframe['REDIRECT_URL'] = og_url
    if a <= 10 or (a <= 100 and a % 10 == 0) or (a <= 1000 and a % 100 == 0) or (a > 1000 and a % 500 == 0):
        print("finished scraping %s listings" % str(a))
    return pdframe


size_of_data = len(pd_listings_report)
print("Number of listings in report: %s" % str(size_of_data))
NUMBER_OF_SLICES = 1 if size_of_data < 100 else 5 if size_of_data < 1000 else 20
slice_size = int(size_of_data / NUMBER_OF_SLICES)
pd_listings_report[['URL_TITLE', 'REDIRECT_URL']] = None, None

for x in range(NUMBER_OF_SLICES):
    starting_number = x * slice_size
    ending_number = None if x == NUMBER_OF_SLICES else slice_size + x * slice_size
    ebay1 = pd_listings_report[starting_number:ending_number]
    try:
        ebay1 = ebay1.apply(extract_title, axis=1)
    except requests.exceptions.MissingSchema:
        print("There are empty lines, please delete or fix them")
    pd_listings_report.update(ebay1, overwrite=True)
    pd_listings_report.to_excel("in_progress.xlsx", index=False)

excel_from_dataframe(pd_listings_report, "scraped_titles_")
os.remove("in_progress.xlsx")
input("Program finished! Thank you")
