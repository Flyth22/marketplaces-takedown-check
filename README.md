# marketplaces-takedown-check
A set of tools I use for work as Data Analyst. Scripts included so far:

1. Blacklisted keywords check - It compares words found in relevant marketplace data titles to titles of spam listings. Returns list of words that could be blacklisted. Certain treshhold is used for listings that were wrongly labeled as relevant.
2. Jira.csv parser - Most valuable data is stored as text in jira's "description" field. This parser transforms this data to different columns in excel file, making it more readable and easier to work with.
3. Title scraper - A simple scraper using Async library. It takes excel report as input and scrapes URL and Title from each URL using simple aiohttp request. Returns excel file with scraped data in columns. The purpose is to find marketplace listings that are no longer active.

