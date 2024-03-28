import requests
from bs4 import BeautifulSoup
import pandas as pd

total_page = 3619 #enter the ammount of total pages to scrap
current_page = 1

data = [] 

while current_page <= total_page:
    url = f"https://www.mobil123.com/mobil-dijual/indonesia?page_number={current_page}&page_size=25"
    req = requests.get
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}
    page_request = requests.get(url, headers=headers)
    soup = BeautifulSoup(page_request.content, "html.parser")
    for e in soup.select('article.listing'):
      words = e.h2.get_text(strip=True).split()
      type_words = [word for word in words[1:5] if not any(char.isdigit() and char != '.' for char in word)]
      d = {
            'tahun': words[0],
            'produk': words[1],
            'type': ' '.join(type_words),
            'harga': e.find('div', {'class' : 'listing__price delta weight--bold'}).get_text(strip=True) if e.find('div', {'class' : 'listing__price delta weight--bold'}) else None
            #adjust accordingly

      }
      d.update({e.get('class')[-1].split('--')[-1]:e.next for e in soup.select('.listing__specs i') if not 'thumb' in e.get('class')[-1]})
      data.append(d)
    current_page += 1

abc = pd.DataFrame(data)