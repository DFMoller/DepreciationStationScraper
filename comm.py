import requests, json

BASE = "http://dfmoller.pythonanywhere.com/"

colors = ["black", "red", "blue", "grey", "orange", "silver", "white"]
years = [2015, 2016, 2017, 2018, 2019, 2020]

for color in colors:
    for year in years:
        response = requests.post(BASE + "addSearch", {"color": color, "year": year})
        print(response.json())

def getSearches():
    response = requests.get(BASE + "getSearches")
    return response.json()

def postReadings(post_data):
    json_list = json.dumps(post_data)
    response = requests.post(BASE + "addReadings", {"data": json_list})
    return response.json()
    
