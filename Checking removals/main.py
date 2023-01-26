import subprocess


def choose_script():
    try:
        number = int(input())
        if number in [1, 2, 3]:
            return number
        else:
            print("input 1,2 or 3")
            return choose_script()
    except ValueError:
        print("input 1,2 or 3")
        return choose_script()


print("""Welcome to my work helper, here are current functions:
1. Check blacklisted keywords in a project
2. Parse Jira.csv file
3. Scrape titles and urls to check for removals
        
Enter number and press enter:""")


scripts_dictionary = {1: "Blacklisted.py",
                      2: "Jira_parse.py",
                      3: "TitleScrape.py"}
s = choose_script()

if s == 1:
    import Blacklisted
if s == 2:
    import Jira_parse
if s == 3:
    import TitlScrape
else:
    print("something went wrong")





