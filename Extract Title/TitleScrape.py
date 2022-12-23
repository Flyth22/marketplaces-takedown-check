from bs4 import BeautifulSoup
import pandas as pd
import requests
import openpyxl

pd.options.mode.chained_assignment = None  # default='warn'

report_path = input("Please paste path to your report excel file: ")
report_path = report_path.replace('"', '')
pd_listings_report = pd.read_excel(report_path, header=4, usecols=[i for i in range(11) if i != 0],
                                   engine='openpyxl')
file_name = "extracted_" + str(report_path.split('\\')[-1])
pd_listings_report = pd_listings_report[pd_listings_report['URL'].astype(bool)]
#headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}


def extract_title(pdframe):
    url = pdframe['URL']
    a = pdframe.name
    og_url = "not found"

    try:
        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.text, features="html.parser")
        og_url = response.url
        title = soup.find("title").text
    except AttributeError:
        title = "Check Manually: attribute error"
    except rTitleScrape.pyequests.exceptions.Timeout as err:
        title = err
    except requests.exceptions.ConnectionError:
        title = "Check Manually: SSLError"
    pdframe['URL_Title'] = title
    pdframe['Redirect_Url'] = og_url
    if a <= 10 or (a <= 100 and a % 10 == 0) or (a <= 1000 and a % 100 == 0) or (a > 1000 and a % 500 == 0):
        print("finished scraping %s listings" % str(a))
    return pdframe


size_of_data = len(pd_listings_report)
print("Number of listings in report: %s" % str(size_of_data))
NUMBER_OF_SLICES = 1 if size_of_data < 100 else 5 if size_of_data < 1000 else 20
pd_listings_report[['URL_Title', 'Redirect_Url']] = None, None

for x in range(NUMBER_OF_SLICES):
    slice_size = int(size_of_data / NUMBER_OF_SLICES)
    starting_number = 0 + x * slice_size
    ending_number = None if x > NUMBER_OF_SLICES or NUMBER_OF_SLICES == 1 else slice_size + x * slice_size
    ebay1 = pd_listings_report[starting_number:ending_number]
    try:
        ebay1 = ebay1.apply(extract_title, axis=1)
    except requests.exceptions.MissingSchema:
        print("There are empty lines, please delete or fix them")
    pd_listings_report.update(ebay1, overwrite=True)
    pd_listings_report.to_excel(file_name, index=False)

input("Program finished! Thank you")
