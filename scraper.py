from bs4 import BeautifulSoup
import requests
from datetime import datetime, date
# import pandas as pd
# from pandas import DataFrame

from comm import getSearches, postReadings
    
    

def url(color, year, page):
    base = 'https://www.autotrader.co.za/cars-for-sale?'
    page_str = 'pagenumber=' + str(page)
    year_str = 'year=' + str(year) + '-to-' + str(year)
    color_str = "colour=" + color.lower().capitalize()
    return base + page_str + '&' + year_str + '&' + color_str

def sort_data(data):
    sorted_data = sorted(data, key=lambda tup: tup[0])
    return sorted_data

def print_data(data):
    for i in data:
        print("Mileage = " + str(i[0]) + "; Price = " + str(i[1]))


def snapshot_scrape():

    searches = getSearches()

    if not searches:
        print("No Searches Found")

    return_data = []

    for search in searches:
        # print(" ")
        # print(str(search['id']))
        # print(search['color'])
        # print(str(search['year']))
        # print(" ")

        current_url = url(search['color'], search['year'], 1)
        html_text = requests.get(current_url).text
        soup = BeautifulSoup(html_text, 'lxml')
        search_results = soup.find_all('div', class_='e-available m-has-photos')
        page_numbers = soup.find('div', class_='b-pagination-bar').find('div', class_='gm-show-inline-block').findChildren()
        pages = int(page_numbers[-1].text) # finds last item in list
        # pages = len(soup.find('div', class_='b-pagination-bar').find('div', class_='gm-show-inline-block').ul)
        # print(str(pages))

        for p in range(pages):

            if p > 0:
                current_url = url(search['color'], search['year'], p+1)
                html_text = requests.get(current_url).text
                soup = BeautifulSoup(html_text, 'lxml')
                search_results = soup.find_all('div', class_='e-available m-has-photos')

            print("Page: " + str(p+1) + ' -> ' + current_url)

            for index, result in enumerate(search_results):
                # result_text = result.text.lower()
                stats = result.find('span', class_='e-icons').find_all('span')
                link = result.find_all("a", href=True)[0]['href']
                if len(stats) == 3:
                    try:
                        title = result.find('span', class_='e-title').text
                        split_mileage = stats[1].text.replace('km', '').replace(' ', '').split()
                        split_price = result.find('span', class_='e-price').text.replace('R', '').replace(' ', '').split()
                        if len(split_mileage) == 2:
                            mileage = int(split_mileage[0]) * 1000 + int(split_mileage[1])
                        elif len(split_mileage) == 1:
                            mileage = int(split_mileage[0])
                        if len(split_price) == 3:
                            price = int(split_price[0]) * 1000000 + int(split_price[1]) * 1000 + int(split_price[2])
                        elif len(split_price) == 2:
                            price = int(split_price[0]) * 1000 + int(split_price[1])
                        elif len(split_price) == 1:
                            price = int(split_price[0])
                        
                        if mileage > 0 and price > 0:
                            data_node = {
                                "search_id": search['id'],
                                "value": price,
                                "mileage": mileage,
                                "title": title,
                                "date": date.today().strftime("%d/%m/%Y"),
                                "rel_link": link
                            }
                            return_data.append(data_node)
                    except ValueError as err:
                        print("ValueError Exception: " + str(err))
        
    print(len(return_data))

    print(postReadings(return_data))

    # Next step: Write json data back with api
    #  -> Also check if another try / catch block is needed for robustness above




    # print("******************************")

    # current_year =  datetime.now().year
    # years = range(current_year - 5, current_year)

    # for car in cars:

    #     total_data = {}

    #     for year in years:

    #         # Check if entry exists for this date, car and model-year
    #         date = datetime.now().date()
    #         entry = SnapshotValue.query.filter_by(car_id=car.id, date=date, year=year).first()
    #         if entry:
    #             print("Snapshot data has already been entered today!")
    #         else:

    #             try: 
                
    #                 current_url = url(car.body, car.brand, car.model, 1, str(year))
    #                 html_text = requests.get(current_url).text
    #                 soup = BeautifulSoup(html_text, 'lxml')
    #                 search_results = soup.find_all('div', class_='e-available m-has-photos')
    #                 pages = len(soup.find('div', class_='b-pagination-bar').find('div', class_='gm-show-inline-block').ul)

    #                 data = []

    #                 for p in range(pages):
    #                     if p > 0:
    #                         current_url = url(car.body, car.brand, car.model, p+1, str(year))
    #                         html_text = requests.get(current_url).text
    #                         soup = BeautifulSoup(html_text, 'lxml')
    #                         search_results = soup.find_all('div', class_='e-available m-has-photos')

    #                     print("Page: " + str(p+1) + ' -> ' + current_url)
    #                     for index, result in enumerate(search_results):
    #                         result_text = result.text.lower()
    #                         stats = result.find('span', class_='e-icons').find_all('span')
    #                         if car.brand in result_text and len(stats) == 3 or car.model in result_text and len(stats) == 3:
    #                             try:
    #                                 split_mileage = stats[1].text.replace('km', '').replace(' ', '').split()
    #                                 split_price = result.find('span', class_='e-price').text.replace('R', '').replace(' ', '').split()
    #                                 if len(split_mileage) == 2:
    #                                     mileage = int(split_mileage[0]) * 1000 + int(split_mileage[1])
    #                                 elif len(split_mileage) == 1:
    #                                     mileage = int(split_mileage[0])
    #                                 if len(split_price) == 3:
    #                                     price = int(split_price[0]) * 1000000 + int(split_price[1]) * 1000 + int(split_price[2])
    #                                 elif len(split_price) == 2:
    #                                     price = int(split_price[0]) * 1000 + int(split_price[1])
    #                                 elif len(split_price) == 1:
    #                                     price = int(split_price[0])
                                    
    #                                 if mileage > 0 and price > 0:
    #                                     data_node = (mileage, price)
    #                                     data.append(data_node)
    #                             except ValueError as err:
    #                                 print("ValueError Exception: " + str(err))

    #                 sorted_data = sort_data(data)
    #                 if (len(sorted_data) > 50):
    #                     df = pd.DataFrame(sorted_data, columns=["mileage", "price"])
    #                     df = df.sample(n=50)
    #                     tuples = [tuple(x) for x in df.to_numpy()]
    #                     total_data[str(year)] = tuples
    #                 else:
    #                     total_data[str(year)] = sorted_data
                
    #             except AttributeError as err:
    #                 print("Attribute Error: " + str(err))
    #                 print("Problem is probably that there are no cars found... No Data added for the current model year")
    #             except Exception as err:
    #                 print("########################### Unknown Error: " + str(err))
            
    #         store_data(car.id, total_data)
try:
    snapshot_scrape()
except ConnectionError as err:
    print("Connection Error: " + err)
    


