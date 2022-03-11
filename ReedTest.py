from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
from urllib.error import HTTPError
from urllib.error import URLError
import re
import math
import csv
import sys


def log():
    logging.basicConfig(filename = 'reedjobs.log', level = logging.DEBUG, format='%(asctime)s <--> %(name)s <--> %(message)s')
    logger = logging.getLogger(__name__)
    return logger


def pageCheck(logger, job):
    log = logger
    try:
        urlopen(job)
        log.info("Page found!")
    except HTTPError as e:
        log.critical(e)
        log.critical("Try to enter a valid format")
        sys.exit(-1)
    except URLError as f:
        log.critical(f)
        log.critical("Check if the page is not down")
        sys.exit(-1)


def pageCalc(logger, job):
    log = logger
    html = urlopen("{}".format(job))
    #Counts how many jobs one page contains
    bs = BeautifulSoup(html, 'html.parser')
    jobs = bs.find_all('div', class_="col-sm-12 col-md-9 col-lg-9 details")
    pageJobs = int(len(jobs))
    promoted = bs.find_all('label', class_="label label-promoted")
    log.info("Promoted jobs to exclude from the jobs counting: ")
    log.info(len(promoted))
    onePageJobs = pageJobs - int(len(promoted))
    log.info("The number of jobs from one page:")
    log.info(onePageJobs)
    #Gets the number of overall jobs
    totalJobs = bs.find('div', class_="page-counter").text

    cut = re.compile('of\s[0-9].*|.\d+\sjobs')
    n = (str(cut.findall(totalJobs)))
    nr = n.replace(",","")
    number = int(nr[5:-9])
    log.info("The number of overall jobs: ")
    log.info(number)

    page_number = math.ceil(number / onePageJobs)
    log.info("The number of pages that contain the chosen type of job")
    log.info(page_number)

    return page_number

def createCvs():
    with open('reedjobs.csv','w', newline='') as f:
        thewriter = csv.writer(f)
        header = ["Title","Salary","Location","Contract","Remote/Site"]
        thewriter.writerow(header)

def csvDetails(jobType, number):
    html = urlopen("{}?pageno={}".format(jobType, number))
    bs = BeautifulSoup(html, 'html.parser')
    jobs = bs.find_all('div', class_="col-sm-12 col-md-9 col-lg-9 details")
    with open('reedjobs.csv', 'a', newline='') as f:
        thewriter = csv.writer(f)
        for job in jobs:
            try:
                title_ = job.find('h3', class_='title').text
                c_title = " ".join(title_.split())
            except:
                c_title = "N/A"

            try:
                salary_ = job.find('li', class_='salary').text
                c_salary = " ".join(salary_.split())
            except:
                c_salary = "N/A"

            try:
                location_ = job.find('li', class_='location').text
                c_location = " ".join(location_.split())
            except:
                c_location = "N/A"

            try:
                time_ = job.find('li', class_='time').text
                c_time = " ".join(time_.split())
            except:
                c_time = "N/A"

            try:
                remote_ = job.find('li', class_='remote').text
                c_remote = " ".join(remote_.split())
            except:
                c_remote = "N/A"
            list = [c_title, c_salary, c_location, c_time, c_remote]
            thewriter.writerow(list)


def jobDetails(logger, jobType, number):
    log = logger
    html = urlopen("{}?pageno={}".format(jobType, number))
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


job = str(sys.argv[1])

logger = log()
createCvs()
pageCheck(logger, job)
pageNr = pageCalc(logger, job)
for i in range(1, pageNr+1):
    jobDetails(logger, job, i)
for i in range(1, pageNr+1):
    csvDetails(job, i)








