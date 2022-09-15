import requests
import json

def request_api(api):
    res = requests.get(api)
    json = json.loads(res.text)
    return json

def get_weather_data(stationid):
    stationid = str(stationid)
    if stationid[0] in "0123456789":
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?Authorization=CWB-0BFC5710-D0E8-46A4-9B4A-6386C222F445&stationId={stationid}'
        weather_element = ["高度(m)", "風向(度)", "風速(m/s)", "溫度(°C)", "相對濕度(%)", "測站氣壓(百帕)", "日累積雨量(mm)", "小時最大陣風風速(m/s)",
                           "小時最大陣風風向(度)", "小時最大陣風時間(小時分鐘)", "本時最大10分鐘平均風速(m/s)", "本時最大10分鐘平均風向(度)",
                           "本時最大10分鐘平均風速發生時間(小時分鐘)", "小時紫外線指數", "本日最高溫(°C)", "本日最高溫發生時間(小時分鐘)",
                           "本日最低溫(°C)", "本日最低溫發生時間(小時分鐘)", "本日總日照時數(hr)", "十分鐘盛行能見度(km)", "十分鐘天氣現象描述"]
    else:
        url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=CWB-0BFC5710-D0E8-46A4-9B4A-6386C222F445&stationId={stationid}'
        weather_element = ["高度(m)", "風向(度)", "風速(m/s)", "溫度(°C)", "相對濕度(%)", "測站氣壓(百帕)", "日累積雨量(mm)", "小時最大陣風風速(m/s)",
                           "小時最大陣風風向(度)", "小時最大陣風時間(yyyy-MM-ddThh:mm:ss+08:00)", "本日最高溫(°C)", "本日最高溫發生時間(小時分鐘)",
                           "本日最低溫(°C)", "本日最低溫發生時間(小時分鐘)"]

    weather_data = request_api(url)

    # if api server return nothing
    if len(weather_data["records"]["location"]) == 0: return "error"

    list_station = ["station", "station_id", "latitude", "longitude", "latest_update_time"] # ["測站", "測站ID", "緯度", "經度", "最後更新時間"]
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