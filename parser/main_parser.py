from urllib import request

from bs4 import BeautifulSoup
import pandas as pd
import re


def create_database(page_number):
    end = True
    solo_indexes = [0, 1, 3, 4, 5, 6, 7, 8, 9]
    while end:
        rosseti_url = "https://rosseti-lenenergo.ru/planned_work/?PAGEN_1={0}".format(
            page_number
        )
        with request.urlopen(rosseti_url) as rosseti_res:
            page = rosseti_res.read()
        soup = BeautifulSoup(page, 'lxml')
        table = soup.find('table', class_='tableous_facts funds')
        paginator = soup.find('div', class_='page-nav')
        for page in paginator.find('a', class_='active').stripped_strings:
            if int(page) != page_number:
                end = False
        for j in table.find_all('tr')[2:]:
            row_data = j.find_all('td')
            row = []
            count = 0
            for i in row_data:
                values = []
                for d in i.stripped_strings:
                    format_d = re.sub(r'\s+', ' ', d)
                    values.append(format_d)
                if not len(values):
                    row.append(None)
                elif count in solo_indexes:
                    if len(values) == 1:
                        row.append(values[0])
                    else:
                        row.append(None)
                else:
                    row.append(values)
                count += 1
            yield row
        page_number = page_number + 1


def main():
    headers = [
        'region',
        'area',
        'address',
        'start_date',
        'start_time',
        'end_date',
        'end_time',
        'branch',
        'res',
        'comment',
        'fias',
    ]
    mydata = pd.DataFrame(columns=headers)
    data_generator = create_database(1)
    for row in data_generator:
        if len(row) == len(headers):
            length = len(mydata)
            mydata.loc[length] = row
    mydata.to_csv('data/parser_data.csv', index=False)


if __name__ == "__main__":
    main()

