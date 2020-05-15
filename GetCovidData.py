import re
import os
import time
import requests 
import pandas as pd
from bs4 import BeautifulSoup as bs

def replaceChars(text):
    noSym = re.sub(r"[\xa0\s]","_",text)
    return re.sub(r"\/","Per",noSym)


raw = requests.get(r"https://www.worldometers.info/coronavirus/").text
soup = bs(raw)

table = soup.find('table',{'id':'main_table_countries_today'})
header = table.find('thead')

columns = [replaceChars(h.text) for h in header.find_all('th')]

body = table.find_all('tbody')[0]

dataRows = []
for row in body.find_all('tr'):
    if not row.get('style',None):
        row = [td.text for td in row.find_all('td')]
        dataRows.append(row)

os.chdir("WHERE THE OUTPUT CSV WILL BE WRITTEN TO")

df = pd.DataFrame(dataRows,columns=columns)
df.to_csv('CovidData_{}.csv'.format(time.strftime("%Y%m%d")))
print('Done')
