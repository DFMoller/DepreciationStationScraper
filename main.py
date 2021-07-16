import schedule, time
from scraper import initiate_scrape

if __name__ == "__main__":
    initiate_scrape()
    schedule.every().day.at("08:00").do(initiate_scrape())
    while True:
        schedule.run_pending()
        time.sleep(1)