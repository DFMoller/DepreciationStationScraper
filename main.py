import schedule, time, os
from scraper import initiate_scrape, log
<<<<<<< HEAD
from comm import maxRetries

PID = str(os.getppid())
with open('/home/pi/Apps/DepreciationStationScraper/app_id/app.pid', 'w') as file:
    file.write(PID)

def myFunction():
    try:
        initiate_scrape()
        log("Schedule Loop Running")
    except maxRetries as err:
        log(err)
=======

PID = str(os.getppid())
with open('app_id/app.pid', 'w') as file:
    file.write(PID)

def myFunction():
    initiate_scrape()
    log("Schedule Loop Running")
>>>>>>> ad327f40d172fe9b03283d136376dd70c2638db1

if __name__ == "__main__":
    myFunction()
    schedule.every().day.at("07:00").do(myFunction)
    while True:
        schedule.run_pending()
        time.sleep(1)