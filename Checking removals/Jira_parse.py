import re
import pandas as pd
import title_scrape_functions as tsf


def match_regex(string, text):
    pattern = r'(?<=' + re.escape(text) + r'.).*'
    result = re.search(pattern, string)
    if result:
        return result.group(0)


def find_id(string):
    id = match_regex(string, text=":")
    if id:
        return id
    else:
        id = match_regex(string, text="Takedown request for")
        return id


def search_images(string):
    pattern = re.escape("https://marketplace.b-cdn.net/") + r'.*?' + r'webp'
    result = re.search(pattern, string)
    if result:
        return result.group(0)


jira_report = tsf.csv_to_pandas()

parsed_report = pd.DataFrame()

description_data = ["Project name", "Marketplace name", "Removal reason", "Seller name", "Url", "Platform url",
                    "Internal listing ID", "Tags"]

parsed_report["ID"] = jira_report['Summary'].apply(find_id)
for name in description_data:
    parsed_report[name] = jira_report['Description'].apply(match_regex, text=name+":")
parsed_report["Image"] = jira_report['Description'].apply(search_images)

tsf.excel_from_dataframe(parsed_report, "jira_" + parsed_report["Project name"][0] + "_")

input("Program finished! Thank you")
