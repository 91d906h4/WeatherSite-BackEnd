import pandas
import re
import requests
import json

def request_api(api_url):
    # request_api
    weather_res = requests.get(api_url)
    get_weather_json = json.loads(weather_res.text)

    return get_weather_json


def get_weather_data(stationid):
    test = re.search(r'\d+', stationid).group(0)

    if stationid == test:
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-0BFC5710-D0E8-46A4-9B4A-6386C222F445&stationId={stationid} '
        weather_element = ["高度(m)", "風向(度)", "風速(m/s)", "溫度(°C)", "相對濕度(%)", "測站氣壓(百帕)", "日累積雨量(mm)", "小時最大陣風風速(m/s)",
                           "小時最大陣風風向(度)", "小時最大陣風時間(小時分鐘)", "本時最大10分鐘平均風速(m/s)", "本時最大10分鐘平均風向(度)",
                           "本時最大10分鐘平均風速發生時間(小時分鐘)", "小時紫外線指數", "本日最高溫(°C)", "本日最高溫發生時間(小時分鐘)",
                           "本日最低溫(°C)", "本日最低溫發生時間(小時分鐘)", "本日總日照時數(hr)", "十分鐘盛行能見度(km)", "十分鐘天氣現象描述"]
    else:
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-0BFC5710-D0E8-46A4-9B4A-6386C222F445&stationId={stationid} '
        weather_element = ["高度(m)", "風向(度)", "風速(m/s)", "溫度(°C)", "相對濕度(%)", "測站氣壓(百帕)", "日累積雨量(mm)", "小時最大陣風風速(m/s)",
                           "小時最大陣風風向(度)", "小時最大陣風時間(yyyy-MM-ddThh:mm:ss+08:00)", "本日最高溫(°C)", "本日最高溫發生時間(小時分鐘)",
                           "本日最低溫(°C)", "本日最低溫發生時間(小時分鐘)"]

    weather_json = request_api(url)

    list_station = ["測站", "測站ID", "經度", "緯度", "最後更新時間"]
    station_data = [weather_json["records"]["location"][0]["locationName"],
                    weather_json["records"]["location"][0]["stationId"],
                    weather_json["records"]["location"][0]["lat"],
                    weather_json["records"]["location"][0]["lon"],
                    weather_json["records"]["location"][0]["time"]["obsTime"]]
    # station_df
    station_dict = dict(zip(list_station, station_data))
    station_df = pandas.DataFrame(list(station_dict.items()), columns=["name", "value"])
    station_df.index += 1

    # setting weather data
    value = []
    weather_dict = {}

    # get weather data value
    for i in weather_json["records"]["location"][0]["weatherElement"]:
        value.append(i["elementValue"])

    # input data to dict
    weather_dict = dict(zip(weather_element, value))

    # turn dict to dataframe
    weather_df = pandas.DataFrame(list(weather_dict.items()), columns=['name', 'value'])
    weather_df.index += 1

    now_weather = pandas.concat([station_df, weather_df], axis=0)

    return stationid, now_weather