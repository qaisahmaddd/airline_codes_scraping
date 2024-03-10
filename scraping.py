import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
url = f'https://en.wikipedia.org/wiki/List_of_airline_codes'
print(f"Memproses halaman: {url}") 
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    
    if table:
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                row_data = [col.get_text(strip=True) for col in columns]
                data.append(row_data)

column_names = ['iata_code', 'icao_code', 'airline', 'call_sign', 'country/region', 'comments']  

airlines_list = pd.DataFrame(data, columns=column_names)
airlines_list.replace('', pd.NA, inplace=True)
airlines_list = airlines_list.dropna(subset=['iata_code'])
airlines_list.drop(['icao_code', 'call_sign'], axis= 1, inplace= True)
airlines_list.to_csv('./airlines_list.csv', index=False)

print("Scraping selesai. Data disimpan ke 'airport_list.csv'")