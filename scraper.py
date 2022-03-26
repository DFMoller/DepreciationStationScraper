from bs4 import BeautifulSoup
import requests
from datetime import date, datetime
from comm import addSearches, getSearches, postReadings, postHistory, deleteOldEntries

def url(color, year, page):
    base = 'https://www.autotrader.co.za/cars-for-sale?'
    page_str = 'pagenumber=' + str(page)
    sort_str = 'sortorder=Newest'
    year_str = 'year=' + str(year) + '-to-' + str(year)
    color_str = "colour=" + color.lower().capitalize()
    return base + page_str + '&' + sort_str + '&' + year_str + '&' + color_str

def log(message):
    # /home/pi/Apps/DepreciationStationScraper/
<<<<<<< HEAD
    with open("/home/pi/Apps/DepreciationStationScraper/log/" + datetime.now().strftime("%Y-%m-%d") + ".txt", "a") as f:
=======
    with open("log/" + datetime.now().strftime("%Y-%m-%d") + ".txt", "a") as f:
>>>>>>> ad327f40d172fe9b03283d136376dd70c2638db1
        print(message)
        print(message, file=f)

def scrape():
    
    log("Adding New Searches on: " + datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))
    addSearches()
    
    log("Fetching All Searches on: " + datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))
    searches = getSearches()

    if not searches:
        log("ERROR: No Searches Found")

    log("Scraping...")
    
    final_data = {}

    for search in searches:
        return_data = []
        current_url = url(search['color'], search['year'], 1)
        
        log("\nScraping for search_id = " + str(search['id']))
        
        while True:
            try:
                html_text = requests.get(current_url).text
                break
            except (requests.ConnectionError, requests.Timeout) as exception:
                log("Error: " + str(exception))
                log("Request Causing the error: scrape() -> search_id = " + str(search["id"]))
            
        soup = BeautifulSoup(html_text, 'lxml')
        search_results = soup.find_all('div', class_='e-available m-has-photos')
        page_numbers = soup.find('div', class_='b-pagination-bar').find('div', class_='gm-show-inline-block').findChildren()
        pages = int(page_numbers[-1].text) # finds last item in list

        for p in range(pages):

            if p > 0:
                current_url = url(search['color'], search['year'], p+1)
                
                while True:
                    try:
                        html_text = requests.get(current_url).text
                        break
                    except (requests.ConnectionError, requests.Timeout) as exception:
                        log("Error: " + str(exception))
                        log("Request Causing the error: scrape() -> search_id = " + str(search["id"]) + " & page = " + str(p))
                              
                soup = BeautifulSoup(html_text, 'lxml')
                search_results = soup.find_all('div', class_='e-available m-has-photos')

#             log("Page: " + str(p+1) + ' -> ' + current_url)

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
                        log("ValueError Exception: " + str(err))
        
        log("Number of Results for search_id = " + str(search['id']) + ": " + str(len(return_data)))
    
        log("Posting Data to DepreciationStation for search_id = " + str(search["id"]))

        log(postReadings(return_data))
        
        final_data[search["id"]] = return_data
    
    log("Posting History Data...")
    log(postHistory(final_data))
    log("History Added")
    
    log("Deleting old entries...")
    log(deleteOldEntries())
    

def initiate_scrape():
    
    url = "http://www.kite.com"
    timeout = 5
    
    log("\n******************************")
    log("Initiating New Scrape Sequence on: " + datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))
    log("******************************")
<<<<<<< HEAD
    flag = False
    log("No internet connection.")
=======
>>>>>>> ad327f40d172fe9b03283d136376dd70c2638db1
    while True:
        try:
            request = requests.get(url, timeout=timeout)
            log("Connected to the Internet")
            break
        except (requests.ConnectionError, requests.Timeout) as exception:
<<<<<<< HEAD
            # No connection
            pass
=======
            log("No internet connection.")
>>>>>>> ad327f40d172fe9b03283d136376dd70c2638db1
            
    log("Starting Scrape...")
    scrape()
    log("Scrape Finished: " + datetime.now().strftime("%Y-%m-%d, %H:%M:%S"))
