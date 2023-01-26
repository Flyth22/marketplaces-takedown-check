from bs4 import BeautifulSoup
import pandas as pd
import requests
from collections import Counter
import time
import openpyxl


def csv_to_pandas():
    report_path = input("Please paste path to your jira.csv file: ")
    report_path = report_path.replace('"', '')
    try:
        pd_listings_report = pd.read_csv(report_path)
        return pd_listings_report
    except FileNotFoundError:
        print("Enter correct file path")
        csv_to_pandas()


def excel_to_pandas():
    report_path = input("Please paste path to your report excel file and press enter: ")
    report_path = report_path.replace('"', '')
    try:
        pd_listings_report = pd.read_excel(report_path, header=4, usecols=[i for i in range(11) if i != 0],
                                           engine='openpyxl')
        return pd_listings_report
    except FileNotFoundError:
        print("Enter correct file path")
        excel_to_pandas()
    #file_name = "extracted_" + str(report_path.split('\\')[-1])


def loop_counter(pdframe):
    a = pdframe.name
    if a <= 10 or (a <= 100 and a % 10 == 0) or (a <= 1000 and a % 100 == 0):
        print("finished scraping %s listings" % str(a))


def extract_title(pdframe):
    url = pdframe['URL']
    og_url = "not found"

    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, features="html.parser")
        og_url = response.url
        title = soup.find("title").text
    except AttributeError:
        title = "Check Manually: attribute error"
    except requests.exceptions.Timeout as err:
        title = err
    except requests.exceptions.ConnectionError:
        title = "Check Manually: SSLError"
    loop_counter(pdframe)
    pdframe['URL_Title'] = title
    pdframe['Redirect_Url'] = og_url

    return pdframe


'''def check_removals(pdframe):
    pdframe[['page title', 'page url', 'out of stock text', 'is listing removed?']] = None, None, None, None
    pdframe = pdframe.sort_values(by="Site")
    marketplaces = pdframe["Site"].unique().tolist()
    for site in marketplaces:
        pd_frame_slice = pdframe[["Site" == site]]
        if site in supported_sites.values():
            pd_frame_slice = pd_frame_slice.apply(supported_sites[site](), axis=1)
        else:
            pd_frame_slice = pd_frame_slice.apply(extract_title, axis=1)
    pdframe.update(pd_frame_slice)
    pdframe.to_excel(file_name, index=False)'''


def make_list(dictionary):
    x = list()
    for word in dictionary:
        x.append(word)
    return x


def show_blacklisted(thrash, accepted, number_of_words=50, error_boundary=0):
    accepted['word_count'] = accepted['Title'].apply(lambda x: x.strip("'").lower().split())
    thrash['word_count'] = thrash['Title'].apply(lambda x: x.strip("'").lower().split())
    accepted_words = [item for sublist in accepted['word_count'] for item in sublist]
    thrash_words = [item for sublist in thrash['word_count'] for item in sublist]

    accepted_dict = dict(Counter(accepted_words))
    accepted_words = [x for x in accepted_dict if accepted_dict[x] >= error_boundary]

    set_accepted_words = set(accepted_words)
    set_thrash_words = set(thrash_words)

    # blacklisted words are those that appear in Thrash but not in Accepted
    blackl = list(set_thrash_words.difference(set_accepted_words))

    # counts how many times each word appears in thrash folder
    thrash_dict = dict(Counter(thrash_words))

    d_frame_blacklisted = pd.DataFrame()
    d_frame_blacklisted["Words"] = blackl
    d_frame_blacklisted["count"] = d_frame_blacklisted["Words"].apply(lambda x: thrash_dict[x])
    d_frame_blacklisted = d_frame_blacklisted.sort_values("count", ascending=False)
    return d_frame_blacklisted.head(number_of_words)


def excel_from_dataframe(dataframe, name):
    filename = name + time.strftime("%Y%m%d-%H%M%S")
    return dataframe.to_excel(filename + ".xlsx", index=False)


#supported_sites = {"Ebay" : ebay, "Redbubble" : redbubble}
