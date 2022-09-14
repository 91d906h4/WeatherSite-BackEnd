import requests
import bs4
import pandas as pd


def get_url_return_soup_table(url):
    html = requests.get(url)
    html.encoding = "utf-8"
    soup = bs4.BeautifulSoup(html.text, 'html.parser')
    return soup.table


def split_list(datalist, n):
    # 將list分割 (l:list, n:每個matrix裡面有n個元素)
    for idx in range(0, len(datalist), n):
        yield datalist[idx:idx + n]


def get_data():
    # main code
    now_exist_station_table = get_url_return_soup_table('https://e-service.cwb.gov.tw/wdps/obs/state.htm#description')

    # find columns list
    search_columns = now_exist_station_table.find_all('th')
    columns_list = []
    for element in search_columns:
        columns_list.append(element.text)

    # find all station data
    data = now_exist_station_table.find_all('td')
    data_list = []

    for element in data:
        if element.text == "":
            data_list.append("無")
        else:
            data_list.append(element.text)

    # split every station data
    data_list = list(split_list(data_list, 12))

    # create dataframe to input data
    station_form = pd.DataFrame(list(data_list), columns=columns_list)

    station_form.index += 1

    # output data
    return station_form


def output_html():
    station_data = get_data()
    result = station_data.to_html(classes="station_table_css_1")
    return result