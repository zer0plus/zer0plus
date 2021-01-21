from bs4 import BeautifulSoup
import requests
import json
import time


watchlist = ['GSAH', 'GIK', 'XL', 'THCB', 'TTCF']
# def watchlist_maker():
    

#     return watchlist


def scrape_data(ticker):
    url = f'https://finance.yahoo.com/quote/{ticker}'
    r = requests.get(url)
    data = BeautifulSoup(r.text, 'html.parser')
    equity = {
    '$ticker' : ticker,
    'price' : data.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[0].text,
    'change' : data.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('span')[1].text,
    '52 Week-range' : data.find('table', {'class': 'W(100%)'}).find_all('td')[11].text
}
    return equity 

def process():
    datalist = []
    for tkr in watchlist:
        datalist.append(scrape_data(tkr))
        print('Scraping: ', tkr)
    le_dict = {}
    for tkr in datalist:
        for k, v in (tkr.items()):
            if (k == '$ticker'):
                tempp = v 
            if (k == '52 Week-range'):
                hooh = (v.split('-'))
                le_dict[tempp] = hooh
    # print(le_dict)
    return datalist, le_dict

def main():
    dl = process()
    soup1 = dl[0] 
    soup2 = dl[1]
    print (soup2) 
    print(float(soup2['GSAH'][1]) - float((soup1[0]['price'])))
    
    with open('dailyreport.json', 'w') as df:
        for tkr in soup1:
            json.dump(tkr, df, indent = 2) 

if __name__ == "__main__":
    main()