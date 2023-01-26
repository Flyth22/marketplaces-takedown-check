import re
import pandas as pd
import title_scrape_functions as tsf


def match_regex(string, text):
    pattern = r'(?<=' + re.escape(text) + r'.).*'
    result = re.search(pattern, string)
    if result:
        return result.group(0)


def find_id(string):
    ID = match_regex(string, text=":")
    if ID:
        return ID
    else:
        ID = match_regex(string, text="Takedown request for")
        return ID


def search_images(string):
    pattern = re.escape("https://marketplace.b-cdn.net/") + r'.*?' + r'webp'
    result = re.search(pattern, string)
    if result:
        return result.group(0)


jira_report = tsf.csv_to_pandas()

parsed_report = pd.DataFrame()


parsed_report["ID"] = jira_report['Summary'].apply(find_id)
parsed_report["Project name"] = jira_report['Description'].apply(match_regex, text="Project name:")
parsed_report["Marketplace name"] = jira_report['Description'].apply(match_regex, text="Marketplace name:")
parsed_report["Removal reason"] = jira_report['Description'].apply(match_regex, text="Removal reason:")
parsed_report["Seller name:"] = jira_report['Description'].apply(match_regex, text="Seller name:")
parsed_report["Url"] = jira_report['Description'].apply(match_regex, text="Url:")
parsed_report["Platform url"] = jira_report['Description'].apply(match_regex, text="Platform url:")
parsed_report["Internal listing ID"] = jira_report['Description'].apply(match_regex, text="Internal listing ID:")
parsed_report["Tags"] = jira_report['Description'].apply(match_regex, text="Tags:")
parsed_report["Image"] = jira_report['Description'].apply(search_images)


parsed_report.to_excel("jira_parsed.xlsx", index=False)

input("Program finished! Thank you")
