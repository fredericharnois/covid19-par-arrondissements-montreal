#!/usr/bin/python
from bs4 import BeautifulSoup
import csv
import requests
import unicodedata
import re
import datetime



url = 'https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/'
response = requests.get(url, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.findAll('table', attrs={'class':'contenttable'})[2]

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
date = yesterday.strftime('%Y-%m-%d')

output_rows = [['Arrondissements', 'Cas Confirmés']]
for table_row in table.findAll('tr'):
    columns = table_row.findAll('td')[0:2]
    output_row = []
    for column in columns:
        column_text = column.text
        column_text = unicodedata.normalize('NFKD', column_text).strip()
        column_text = column_text.replace('*', '')
        if re.search('[a-zA-Z]', column_text) is None:
            column_text = column_text.replace(' ', '')
        elif column_text == 'Territoire à confirmer2':
            column_text = column_text.replace('2', '')
        output_row.append(column_text)
    output_rows.append(output_row)
output_rows = filter(None, output_rows)
    
with open('data\\' + str(date) + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)