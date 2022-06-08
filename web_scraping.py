####################****   Web Scraping   *****########################################################################
###  We want to prepare data base for our DSA Search Engine
########  Importing all the required Modules
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import lxml.html
import lxml.html.clean
def cleanHTML(html):
    doc = lxml.html.fromstring(html)
    cleaner = lxml.html.clean.Cleaner(style=True)
    doc = cleaner.clean_html(doc)
    s = doc.text_content()
    u = ""
    for c in s:
        if ord(c) < 128:
            u += c
        else:
            u += " "
    return u

driver = webdriver.Chrome(ChromeDriverManager().install())


#############################  Scraping problem urls and Titles and problem Content  ######################################################
############  Link inside get()  is the website from where you want ro scrape titles and urls
###########  We can scrape from multiple website but then we need to take care of Indexing

driver.get("https://www.codechef.com/tags/problems/dynamic-programming")
# As we want to give some time to webdriver to read the html page of the website
# (in case you Internet is slow you can increase the sleep time otherwise it may throw error)
time.sleep(20)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')  ####  Using B4S to parse the html page obtained

######  Obtaining   url.txt and title.txt for all the problems
all_ques_div = soup.findAll("div", {"class": "problem-tagbox-inner"})
all_ques = []
for ques in all_ques_div:
	all_ques.append(ques.findAll("div")[0].find("a"))
urls = []
titles = []
for ques in all_ques:
	urls.append("https://www.codechef.com"+ques['href'])
	titles.append(ques.text)
print(len(urls));
with open("DataBase\problem_urls.txt", "w+") as f:
	f.write('\n'.join(urls))

with open("DataBase\problem_titles.txt", "w+") as f:
	f.write('\n'.join(titles))


################  Preparing problem_Content folder  which will contain number of files = number of problem_urls scraped
####### where each file will contaion description of single problem
####### Remember to take care of index
import numpy as np
### Obtaining Problem_url.txt as an array of urls with length = number of problems scraped
Data = np.genfromtxt("Database/Problem_urls.txt", dtype=str)
cnt = 0
for url in Data:
    cnt +=1
    # if cnt2>2:
    #     continue
    driver.get(url)  # opening the webdriver for the given url
    time.sleep(5)     # gioing through html of this web page
    html = driver.page_source   # obtaining the html
    soup = BeautifulSoup(html, 'html.parser')   # Parsing out html content using B4S
    problem_text = soup.find('div', {"class": "problem-statement"}).get_text()   # Getting text content of the div with given class
    problem_text = problem_text.encode("utf-8")  # applying utf-8 encoding required if we want to save it as txt file
    problem_text = str(problem_text)  # conterverting it into string and it is also required if we want to write this content in a txt.file
    #####  Writing problem_content for each problem as a separate file with ****taking care of index
    with open("DataBase/Problem_Content/problem_" + str(cnt) + ".txt", "w+") as f:
        f.write(problem_text)

#####################################################
###### With this code we were able to obtain :-
#####  1) Problem_titles.txt
#####  2) Problem_urls.txt
#####  3) Problem_Content folder containing problem_content of each problem as a seperate file

#***********  For further usage   we also want to obtain Problem_titles folder and Problem_url folder.
# which contain problem title and url respectively for each problem as a seperate file.
######### We did so using code below
file1 = open('DataBase/Problem_titles.txt', 'r')
Lines = file1.readlines()
# Strips the newline character
cnt = 0
for line in Lines:
    cnt += 1
    with open("Problem_Set/Problem_titles/problem_title_"+ str(cnt) + ".txt", "a+") as f:
        f.write(line)

file1 = open("DataBase/Problem_urls.txt", 'r')
Lines = file1.readlines()
# Strips the newline character
cnt =0
for line in Lines:
    cnt += 1
    # if cnt > x:
    #     break
    with open("Problem_Set/Problem_urls/problem_url_" + str(cnt) + ".txt", "a+") as f:
        f.write(line)