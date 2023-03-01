# marketplaces-takedown-check
A set of tools I use to make my work easier. It's a learning code with mix of things I've learned so far. Features included so far:

1. Blacklisted keywords check - It compares words found in relevant marketplace data titles to titles of spam listings. Returns list of words that could be blacklisted. Certain treshhold is used for listings that were wrongly labeled as relevant.
2. Jira.csv parser - Most valuable data is stored as text in jira's "description" field. This parser transforms this data to different columns in excel file, making it more readable and easier to work with.
3. Title scraper Async - A simple scraper using Async library. It takes excel report as input and scrapes URL and Title from each URL using simple aiohttp request. Returns excel file with scraped data in columns. The purpose is to find marketplace listings that are no longer active.
4. Title scraper slow - same as previous but without asyncio library, so it extremely slow. It's better to use this one for large volume of URLs from single page, to lower the chance of block.
