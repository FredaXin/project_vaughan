from bs4 import BeautifulSoup
import requests
import csv

source = requests.get('https://www12.statcan.gc.ca/census-recensement/2006/dp-pd/hlt/97-550/Index.cfm?TPL=P1C&Page=RETR&LANG=Eng&T=307&S=3&O=D&RPP=699').text
soup = BeautifulSoup(source, 'lxml')


table = soup.find('table')
tbody = table.find('tbody')
list_of_rows = tbody.findChildren('tr')


dict_list = []
for row in list_of_rows:
    new_dict = {}

    csd = row.find('th', class_=lambda cs: cs is not None and 'ROWSTUBCELLMONO' in cs)
    new_dict['CSD'] = csd.text.split('\xa0')[0] if csd is not None else None

    pop_2006 = row.find('td', headers=lambda hs: hs is not None and "col_2_1" in hs)
    new_dict['2006'] = pop_2006.text if csd is not None else None

    pop_2001 = row.find('td', headers=lambda hs: hs is not None and "col_2_2" in hs)
    new_dict['2001'] = pop_2001.text.split('\xa0')[0] if csd is not None else None

    dict_list.append(new_dict)


keys = dict_list[0].keys()
with open('census_2006_2001.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dict_list)
