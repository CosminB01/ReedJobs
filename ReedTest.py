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



def getPage(jobtype, logger):
    log = logger
    try:
        html_ = urlopen("https://www.reed.co.uk/jobs/{}?pageno=1".format(jobtype))
        log.info("Page found!")
    except HTTPError as e:
        log.critical(e)
        log.critical("Try to enter a valid format")
        sys.exit(-1)
    except URLError as f:
        log.critical(f)
        log.critical("Check if the page is not down")
        sys.exit(-1)
    return html_


def pageCalc(logger, link):
    log = logger
    html = link

    #Counts how many jobs exists on a job page
    bs = BeautifulSoup(html, 'html.parser')
    jobs = bs.find_all('div', class_="col-sm-12 col-md-9 col-lg-9 details")
    onePageJobs = int(len(jobs))
    log.info("The number of jobs from one page:")
    log.info(onePageJobs)

    #Gets the number of overall jobs
    totalJobs = str(bs.find('div', class_="page-counter"))

    cut = re.compile('of\s[0-9],\d+\sjobs')
    n = (str(cut.findall(totalJobs)))
    number = int(n[4:-6].replace(",", ""))

    page_number = math.ceil(number / onePageJobs)
    log.info(page_number)

    return page_number





def jobDetails(logger, link):
    log = logger
    html = link
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
            salary = job.find('li', class_='salary').text
        except:
            salary = "cannot extract job's salary -- not found"
        s = "Extracted job's salary value: "
        log.info(s + salary)

        try:
            location = job.find('li', class_='location').text
        except:
            location = "cannot extract job's location -- not found"
        l = "Extracted job's location value: "
        log.info(l + location)

        try:
            time = job.find('li', class_='time').text
        except:
            time = "cannot extract job's duration -- not found"
        tme = "Extracted job's time value: "
        log.info(tme + time)

        try:
            remote = job.find('li', class_='remote').text
        except:
            remote = "cannot extract job's type (remote or not) -- not found"
        r = "Extracted job's remote value: "
        log.info(r + remote)





logger = log()
link = getPage('delivery-driver-jobs', logger)
pageNr = pageCalc(logger, link)
jobDetails(logger, link)
#csv(logger)




