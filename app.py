from bs4 import BeautifulSoup
import csv
import requests
import unicodedata
import re
import dateparser


url = 'https://santemontreal.qc.ca/population/coronavirus-covid-19/'
response = requests.get(url, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.findAll('table', attrs={'class':'contenttable'})[1]

date_text = soup.find(text=re.compile('Fichier du DCIMI, en date du'))
french_date = re.search(r'(?<=en date du ).*?(?= 1)', date_text).group(0)
date = dateparser.parse(french_date + ' 2020').date()

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
        output_row.append(column_text)
    output_rows.append(output_row)
output_rows = filter(None, output_rows)
    
with open('data\\' + str(date) + '.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)