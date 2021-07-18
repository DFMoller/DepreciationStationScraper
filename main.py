import schedule, time
from scraper import initiate_scrape

def myFunction():
    initiate_scrape()
    print("Schedule Loop Running")

if __name__ == "__main__":
    myFunction()
    schedule.every().day.at("07:00").do(myFunction)
    while True:
        schedule.run_pending()
        time.sleep(1)