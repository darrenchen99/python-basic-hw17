import csv
import requests
from bs4 import BeautifulSoup
# Web site for download data
url = 'https://www.findrate.tw/USD/#.XhGik0czaUk'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
# Request to get data from Web site
resp = requests.get(url, headers=headers)
resp.encoding = 'utf-8'
raw_html = resp.text
soup = BeautifulSoup(raw_html, 'html.parser')
def parse_str_to_float(raw_value):
    return float(raw_value)
# Analyze data and use selector to search the data you need
usd_list = []
for index in range(2,40):
    #print('index:', index)
    usd_dict = {}
    usd_dict['bank'] = soup.select(f'#right > table:nth-child(12) > tbody > tr:nth-child({index}) > td.bank > a')[0].text
    usd_dict['spot_exchange_rate_sell'] = parse_str_to_float(soup.select(f'#right > table:nth-child(12) > tbody > tr:nth-child({index}) > td:nth-child(5)')[0].text)
    usd_list.append(usd_dict)
# Write data to file with csv format
headers = ['bank', 'spot_exchange_rate_sell']
with open('usd_exchange.csv', 'w') as output_file:
  dict_writer = csv.DictWriter(output_file, headers)
  dict_writer.writeheader()
  dict_writer.writerows(usd_list)
# Find three banks with the lowest exchange rate for USD
exchange_rate_list = []
for z1 in range(38):
  exchange_rate = usd_list[z1]['spot_exchange_rate_sell']
  exchange_rate_list.append(exchange_rate)
exchange_rate_list_sorted = sorted(exchange_rate_list)
for z2 in range(3):
  for z3 in range(38):
    if exchange_rate_list_sorted[z2] == usd_list[z3]['spot_exchange_rate_sell']:
      goodbank = usd_list[z3]['bank']
      lower_exchange_rate = usd_list[z3]['spot_exchange_rate_sell']
      print(goodbank, lower_exchange_rate)
      break
print('These three banks have the lowest US$ spot exchange rate for user to buy in.')