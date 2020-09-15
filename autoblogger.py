import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
import bs4
import requests
from datetime import date
import nltk
from newspaper import Article

urlist = []
res = requests.get('https://www.cnn.com/business')
soup = bs4.BeautifulSoup(res.text,'lxml')
pattern = str(date.today())
pattern = pattern.replace('-','/',3)
pattern = '/' + pattern + '/' + '\w+/\w+/index.html'
soup = str(soup).replace('-','_')
for i in re.finditer(pattern, soup):
    url = str(i.group())
    url = url.replace('_','-')
    urlist.append(url)
urlist = list(set(urlist))

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
'''
================================
In the line below you will need to insert your own json file name
This file name can be obtained from the google apis page
================================
'''
creds = ServiceAccountCredentials.from_json_keyfile_name("ENTER YOUR JSON FILE NAME", scope)
client = gspread.authorize(creds)
'''
In the line below you will need to put the name of the excel file to write to in the quotes
'''
sheet = client.open("ENTER YOUR GOOGLE SHEETS FILE NAME").sheet1

for i in range(len(urlist[:10])):
    
    # Get the article
    url = 'https://www.cnn.com' + urlist[i]
    article = Article(url)
    
    # Do some NLP
    article.download()
    article.parse()
    nltk.download('punkt')
    article.nlp()
    
    title = 'CNN Summarized: ' + article.title + ' by: ' + str(article.authors[0])
    
    date = str(article.publish_date).replace('-','/',3)[:10]
    
    row = [title, article.summary, article.top_image, date, str(article.authors[0])]
    
    sheet.insert_row(row)