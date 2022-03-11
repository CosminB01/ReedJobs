from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
from urllib.error import HTTPError
from urllib.error import URLError
import re
import math
from csv import writer
import sys


def log():
    logging.basicConfig(filename = 'reedjobs.log', level = logging.DEBUG, format='%(asctime)s <--> %(name)s <--> %(message)s')
    logger = logging.getLogger(__name__)
    return logger

def csv(logger,list):
    log = logger
    with open('reedjobs.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['Title', 'Location', 'Salary', 'Duration', 'Type']
        writer.writerow(header)
        writer.writerow(list)
    log.info("Created csv")



def pageCalc(logger, job):
    log = logger
    html = urlopen("{}".format(job))

    #Counts how many jobs one page contains
    bs = BeautifulSoup(html, 'html.parser')
    jobs = bs.find_all('div', class_="col-sm-12 col-md-9 col-lg-9 details")
    pageJobs = int(len(jobs))
    promoted = bs.find_all('label', class_="label label-promoted")
    log.info("Promoted jobs to exclude...")
    log.info(len(promoted))
    onePageJobs = pageJobs - int(len(promoted))
    log.info("The number of jobs from one page:")
    log.info(onePageJobs)
    #Gets the number of overall jobs
    totalJobs = str(bs.find('div', class_="page-counter"))

    cut = re.compile('of\s[0-9]\d+\sjobs')
    n = (str(cut.findall(totalJobs)))
    log.info("Extracted the string..")
    log.info(cut)
    nr = n.replace(",","")
    print(nr)
    number = int(nr[4:-6])
    log.info(number)
    log.info("The number of overall jobs: ")
    log.info(number)

    page_number = math.ceil(number / onePageJobs)
    log.info("The number of pages that contain the chosen type of job")
    log.info(page_number)

    return page_number



def jobDetails(logger, jobType, number):
    log = logger
    try:
        html = urlopen(jobType+"{}".format(number))
        log.info("Page found!")
    except HTTPError as e:
        log.critical(e)
        log.critical("Try to enter a valid format")
        sys.exit(-1)
    except URLError as f:
        log.critical(f)
        log.critical("Check if the page is not down")
        sys.exit(-1)
    bs = BeautifulSoup(html, 'html.parser')
    jobs = bs.find_all('div', class_="col-sm-12 col-md-9 col-lg-9 details")
    for job in jobs:
        try:
            title = job.find('h3', class_='title').text
        except:
            title = "cannot extract job's title -- not found"
        tle = "Extracted job's title value: "
        log.info(tle + title)

        try:
            title_ = job.find('h3', class_='title').text
            csv_remote = " ".join(title_.split())
        except:
            csv_remote = "N/A"



        try:
            salary = job.find('li', class_='salary').text
        except:
            salary = "cannot extract job's salary -- not found"
        s = "Extracted job's salary value: "
        log.info(s + salary)

        try:
            salary_ = job.find('li', class_='salary').text
            csv_salary = " ".join(salary_.split())
        except:
            csv_salary = "N/A"



        try:
            location = job.find('li', class_='location').text
        except:
            location = "cannot extract job's location -- not found"
        l = "Extracted job's location value: "
        log.info(l + location)

        try:
            location_ = job.find('li', class_='location').text
            csv_location = " ".join(location_.split())
        except:
            csv_location = "N/A"



        try:
            time = job.find('li', class_='time').text
        except:
            time = "cannot extract job's duration -- not found"
        tme = "Extracted job's time value: "
        log.info(tme + time)

        try:
            time_ = job.find('li', class_='time').text
            csv_time = " ".join(time_.split())
        except:
            csv_time = "N/A"



        try:
            remote = job.find('li', class_='remote').text
        except:
            remote = "cannot extract job's type (remote or not) -- not found"
        r = "Extracted job's remote value: "
        log.info(r + remote)

        try:
            remote_ = job.find('li', class_='remote').text
            csv_remote = " ".join(remote_.split())
        except:
            csv_remote = "N/A"



job = str(sys.argv[1])

logger = log()
pageNr = pageCalc(logger, job)
for i in range(0, pageNr + 1):
    jobDetails(logger, job, i)







