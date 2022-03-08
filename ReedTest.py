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
        urlopen("https://www.reed.co.uk/jobs/{}?pageno=1".format(jobtype))
        log.info("Page found!")
    except HTTPError as e:
        log.critical(e)
        log.critical("Try to enter a valid format")
    except URLError as f:
        log.critical(f)
        log.critical("Check if the page is not down")


def pageCalc(logger, link):
    log = logger
    html = urlopen(link)
    bs = BeautifulSoup(html, 'html.parser')
    job = bs.find_all('div', class_="col-sm-12 col-md-9 col-lg-9 details")
    log.info(job)
    #jobsNumber = (len(job))
    #pageCounter = bs.find('div', class_="page-counter").text
    #totalPages = int(pageCounter[10,-5])
    #log.info(jobsNumber)


logger = log()
link = getPage('delivery-driver-jobs', logger)
pageCalc(logger,link)
#csv(logger)




