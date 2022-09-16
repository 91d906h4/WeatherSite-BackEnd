from collections import defaultdict
import requests
import json
from bs4 import BeautifulSoup

def request_api(api):
    res = requests.get(api)
    data = json.loads(res.text)
    return data

def get_weather_data(stationid):
    stationid = str(stationid)
    if stationid[0] in "0123456789":
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-0BFC5710-D0E8-46A4-9B4A-6386C222F445&stationId={stationid}'
    else:
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-0BFC5710-D0E8-46A4-9B4A-6386C222F445&stationId={stationid}'

    weather_data = request_api(url)

    # if api server return nothing
    if len(weather_data["records"]["location"]) == 0: return {"status": "error"}

    list_station = ["station", "station_id", "latitude", "longitude", "latest_update_time"]
    station_data = [weather_data["records"]["location"][0]["locationName"],
                    weather_data["records"]["location"][0]["stationId"],
                    weather_data["records"]["location"][0]["lat"],
                    weather_data["records"]["location"][0]["lon"],
                    weather_data["records"]["location"][0]["time"]["obsTime"]]
    station_dict = dict(zip(list_station, station_data))

    # set weather data value
    weather_dict = {}
    for i in weather_data["records"]["location"][0]["weatherElement"]:
        weather_dict[i["elementName"]] = i["elementValue"]

    station_dict.update(weather_dict)

    return station_dict

def get_city_station_data(city):
    html = requests.get('https://e-service.cwb.gov.tw/wdps/obs/state.htm#description')
    html.encoding = "utf-8"
    soup = BeautifulSoup(html.text, 'html.parser')

    data = soup.find_all('td')
    data_list = [element.text if element.text != "" else "N/A" for element in data]

    data, temp = defaultdict(list), []
    for i in range(0, len(data_list)):
        if (i - 0) % 12 == 0: temp.append(data_list[i])
        if (i - 5) % 12 == 0:
            temp.append(data_list[i])
            print(temp[1], temp[0])
            data[temp[1]].append(temp[0])
            temp = []

    return data