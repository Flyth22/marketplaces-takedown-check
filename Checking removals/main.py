import openpyxl


def choose_script():
    try:
        number = int(input())
        if number in [1, 2, 3, 4]:
            return number
        else:
            print("input 1,2,3 or 4")
            return choose_script()
    except ValueError:
        print("input 1,2,3 or 4")
        return choose_script()


print("""Welcome to my work helper, here are the current functions:
1. Check blacklisted keywords in a project
2. Parse Jira.csv file
3. Scrape titles and urls - fast version
4. Scrape titles and urls - slow version
        
Enter number and press enter:""")


scripts_dictionary = {1: "Blacklisted.py",
                      2: "Jira_parse.py",
                      3: "TitleScrapeAsync.py",
                      4: "TitleScrapeSlow.py"}
chosen_script = choose_script()

if chosen_script == 1:
    import Blacklisted
if chosen_script == 2:
    import Jira_parse
if chosen_script == 3:
    import TitleScrapeAsync
if chosen_script == 4:
    import TitleScrapeSlow
else:
    print("Something went wrong, try again")

