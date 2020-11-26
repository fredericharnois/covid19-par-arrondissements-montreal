from bs4 import BeautifulSoup
import csv
import requests
import unicodedata
import re
import datetime


url = 'https://santemontreal.qc.ca/population/coronavirus-covid-19/situation-du-coronavirus-covid-19-a-montreal/'
response = requests.get(url, timeout=30)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.findAll('table', attrs={'class': 'contenttable'})[3]

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)
date = yesterday.strftime('%Y-%m-%d')

output_rows = [['Arrondissements', 'Cas Confirmés']]
for table_row in table.findAll('tr'):
    cities = table_row.findAll('td')[0:1]
    cases = table_row.findAll('td')[4:5]
    output_row = []
    for i in range(len(cities)):
        city = cities[i].text
        city = unicodedata.normalize('NFKD', city).strip()
        city = city.replace('*', '')
        if re.search('[a-zA-Z]', city) is None:
            city = city.replace(' ', '')
        elif city == 'Territoire à confirmer3':
            city = city.replace('3', '')
        case_total = cases[i].text
        case_total = case_total.replace(' ', '')
        output_row.append(city)
        output_row.append(case_total)
    output_rows.append(output_row)
output_rows = filter(None, output_rows)

with open('data/' + str(date) + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)
