from urllib.request import Request
import requests, json, datetime
from pandas import DataFrame
from datetime import date, datetime
# from scraper import log

class maxRetries(Exception):
    pass

def log(message):
    with open("/home/pi/Apps/DepreciationStationScraper/log/" + datetime.now().strftime("%Y-%m-%d") + ".txt", "a") as f:
        print(message)
        print(message, file=f)

BASE = "http://dfmoller.pythonanywhere.com/"

colors = ["black", "red", "blue", "grey", "orange", "silver", "white"]
years = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    
def addSearches():
    add_search_error_count = 0
    for color in colors:
        for year in years:
            while True:
                if add_search_error_count > 10:
                    log(f'Adding Search for color: {color} and year: {year} exceeded 10 tries. Raising custom exception!')
                    raise maxRetries(f'Adding Search for color: {color} and year: {year} exceeded 10 failures')
                try:
                    response = requests.post(BASE + "addSearch", {"color": color, "year": year})
                    log(response.json())
                    break
                except (requests.ConnectionError, requests.Timeout) as exception:
                    log("Error: " + str(exception))
                    log("Request Causing the error: Add Search for " + color + " cars from " + str(year))
                except ValueError as err:  # ValueError includes simplejson.decoder.JSONDecodeError
                    log("JSON Decode Error when adding Search: " + str(err))
                    add_search_error_count += 1

def getSearches():
    while True:
        try:
            response = requests.get(BASE + "getSearches")
            return response.json()
            break
        except (requests.ConnectionError, requests.Timeout) as exception:
            log("Error: " + str(exception))
            log("Request Causing the error: GetSearches()")
        except ValueError as err:
            log("JSON Decode Error when fetching Searches: " + str(err))

def postReadings(post_data):
    json_list = json.dumps(post_data)
    while True:
        try:
            response = requests.post(BASE + "addReadings", {"data": json_list})
            return response.json()
            break
        except (requests.ConnectionError, requests.Timeout) as exception:
            log("Error: " + str(exception))
            log("Request Causing the error: PostReadings() -> search_id = " + str(post_data[0]['search_id']))
        except ValueError as err:
            log("JSON Decode Error when posting Readings: " + str(err))
            log("Request Causing the error: PostReadings() -> search_id = " + str(post_data[0]['search_id']))
            log(f'Response from Server: \n\t{response.content}')
            

def postHistory(data):
    
    final_data = {}
    for search_id in data:
        line = []
        for node in data[search_id]:
            instance = (node["value"], node["mileage"], node["date"])
            line.append(instance)
        df = DataFrame(line, columns=["value", "mileage", "date"])
        sorted_df = df.sort_values("value")
        median_value = sorted_df["value"].median()
        final_data[search_id] = {
            "date": date.today().strftime("%d/%m/%Y"),
            "median_value": int(median_value)
        }
        # if search_id == 1:
        #     print(sorted_df)
        #     print("Median Value: " + str(median_value))
    
    while True:
        try:
            response = requests.post(BASE + "addHistory", {"data": json.dumps(final_data)})
            return str(response.json())
            break
        except (requests.ConnectionError, requests.Timeout) as exception:
            log("Error: " + str(exception))
            log("Request Causing the error: PostHistory()")
        except ValueError as err:
            log("JSON Decode Error when posting History: " + str(err))
       
    
#     response = requests.post(BASE + "addHistory", {"data": json.dumps(final_data)})
#     return str(response.json())

def deleteOldEntries():
    while True:
        try:
            response = requests.delete(BASE + "deleteOldEntries")
            return response.json()
            break
        except (requests.ConnectionError, requests.Timeout) as exception:
            log("Error: " + str(exception))
            log("Request Causing the error: deleteOldEntries()")
        except ValueError as err:
            log("JSON Decode Error when deleting old Entries: " + str(err))
