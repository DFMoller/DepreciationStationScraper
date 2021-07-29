import schedule, time, os
from scraper import initiate_scrape, log

PID = str(os.getppid())
with open('app_id/app.pid', 'w') as file:
    file.write(PID)

def myFunction():
    initiate_scrape()
    log("Schedule Loop Running")

if __name__ == "__main__":
    myFunction()
    schedule.every().day.at("07:00").do(myFunction)
    while True:
        schedule.run_pending()
        time.sleep(1)