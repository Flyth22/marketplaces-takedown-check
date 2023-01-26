import pandas as pd
from title_scrape_functions import show_blacklisted
from title_scrape_functions import excel_from_dataframe
import openpyxl


def ta_reports_to_dataframe():
    a = 0
    b = 0
    accepted_pd_parsing = pd.DataFrame()
    trash_pd_parsing = pd.DataFrame()
    while True:
        try:
            acc = pd.read_excel("Accepted"+str(a+1)+".xlsx", header=4, engine='openpyxl', usecols=[i for i in range(11) if i != 0])
            accepted_pd_parsing = accepted_pd_parsing.append(acc, ignore_index=True)
            a += 1
        except IOError:
            print("Number of accept files:"+str(a))
            break

    while True:
        try:
            tt = pd.read_excel("Trash"+str(b+1)+".xlsx", header=4, engine='openpyxl', usecols=[i for i in range(11) if i != 0])
            trash_pd_parsing = trash_pd_parsing.append(tt, ignore_index=True)
            b += 1
        except IOError:
            print("Number of trash files:"+str(b))
            break
    if a == 0 and b == 0:
        input("There are no reports in current folders or they have wrong names. Please check and try again")
        return ta_reports_to_dataframe()
    else:
        accepted_pd_parsing['Category'] = "Accepted"
        trash_pd_parsing['Category'] = "Trash"
        return accepted_pd_parsing, trash_pd_parsing


def get_number_of_words():
    try:
        number = int(input("How many blacklisted words do you want to see? (MAX 10 000) "))
        if number < 0 or number > 10000:
            print("choose a number between 0 and 10 000")
            return get_number_of_words()
        else:
            return number
    except ValueError:
        print("Please write a number")
        return get_number_of_words()


def get_error_boundary():
    try:
        number = int(input("Error Boundary (choose 0 if you dont know) "))
        return number
    except ValueError:
        print("Please write a number")
        return get_error_boundary()


print("All thrash reports need to be named 'Trash1.xlsx', 'Trash2.xlsx' etc. "
      "All Accepted reports need to be named 'Accepted1.xlsx', 'Accepted2.xlsx' etc.")
input("Please, check if files have correct names")
# Tnumber = input("Enter the amount of reports from Trash")
# Anumber = input("Enter the amount of reports from Accepted")

number_of_words_in = get_number_of_words()
error_boundary_in = get_error_boundary()
accepted_pd, trash_pd = ta_reports_to_dataframe()
blacklisted = show_blacklisted(trash_pd, accepted_pd, number_of_words_in, error_boundary_in)
excel_from_dataframe(blacklisted, "blacklisted_")

input("Done! Your top keywords are in new excel file")
