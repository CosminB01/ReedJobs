#importing the libraries that are needed for the scraper

from urllib.request import urlopen
from bs4 import BeautifulSoup
import logging
import re
import math
from csv import writer


#the code that will bring up the jobs and the main details from each page

def pagejob(pageURL):
    html = urlopen('https://www.reed.co.uk/jobs/coding-jobs?pageno={}'.format(pageURL))
    bs = BeautifulSoup(html, 'html.parser')
    soup = bs.find_all('div', class_='col-sm-12 col-md-9 col-lg-9 details')
    list = []
    for work in soup:
        #tries to get the title and if it can't be found, replaces the title with an error string that is shown in the log file
        try:
            title_ = work.find('h3', class_='title').text
        except:
            title_ = "cannot extract job's title - text not found"

        afterTitle = "Extracted job\'s title, value: "
        logging.info(afterTitle + title_)


        #tries to get the title and if it can't be found, replaces the title with an error string that is shown in the csv file
        try:
            title = work.find('h3', class_='title').text
            c_title = " ".join(title.split())
        except:
            c_title = 'N/A'


        #tries to get the salary and if it can't be found, replaces the salary with an error string that is shown in the log file
        try:
            salary_ = work.find('li', class_='salary').text
        except:
            salary_ = 'cannot extract job salary - text not found'
        afterSalary = "Extracted job\'s salary, value: "
        logging.info(afterSalary + salary_)


<<<<<<< HEAD
        # tries to get the salary and if it can't be found, replaces the salary with an error string that is shown in the csv file
=======
        # tries to get the salary and if it isn't found, replaces the salary with an error string that is shown in the csv file
>>>>>>> 75e904c76dfd79ea9aa3e11eed7bee55d5294504
        try:
            salary = work.find('li', class_='salary').text
            c_salary = " ".join(salary.split())
        except:
            c_salary = 'N/A'


        # tries to get the location and if it can't be found, replaces the location with an error string that is shown in the log file
        try:
            location_ = work.find('li', class_='location').text
        except:
            location_ = 'cannot extract job location - text not found'
        afterLocation = "Extracted job\'s location, value: "
        logging.info(afterLocation + location_)


<<<<<<< HEAD
        # tries to get the location and if it can't be found, replaces the location with an error string that is shown in the csv file
=======
        # tries to get the location and if it isn't found, replaces the location with an error string that is shown in the csv file
>>>>>>> 75e904c76dfd79ea9aa3e11eed7bee55d5294504
        try:
            location = work.find('li', class_='location').text
            c_location = " ".join(location.split())
        except:
            c_location = 'N/A'


        # tries to get the time of the job and if it can't be found, replaces the time of the job with an error string that is shown in the log file
        try:
            time_ = work.find('li', class_='time').text
        except:
            time_ = "cannot extract job duration - text not found"
        afterTime = 'Extracted job\'s duration, value: '
        logging.info(afterTime + time_)


<<<<<<< HEAD
        # tries to get the time of the job and if it can't be found, replaces the time of the job with an error string that is shown in the csv file
=======
        # tries to get the time of the job and if it isn't found, replaces the time of the job with an error string that is shown in the csv file
>>>>>>> 75e904c76dfd79ea9aa3e11eed7bee55d5294504
        try:
            time = work.find('li', class_='time').text
            c_time = " ".join(time.split())
        except:
            c_time = "N/A"


<<<<<<< HEAD
        # tries to get the type of the job(remote\site) and if it can't be found, replaces the type of the job(remote\site)
=======
        # tries to get the type of the job(remote\site) and if it isn't found, replaces the type of the job(remote\site)
>>>>>>> 75e904c76dfd79ea9aa3e11eed7bee55d5294504
        # with an error string that is shown in the log file
        try:
            remote_ = work.find('li', calss_='remote').text
        except:
            remote_ = 'cannot extract job type - text not found'
        afterRemote = 'Extracted job\'s type, value: '
        logging.info(afterRemote + remote_)


<<<<<<< HEAD
        # tries to get the type of the job(remote\site) and if it can't be found, replaces the type of the job(remote\site)
=======
        # tries to get the type of the job(remote\site) and if it isn't found, replaces the type of the job(remote\site)
>>>>>>> 75e904c76dfd79ea9aa3e11eed7bee55d5294504
        # with an error string that is shown in the csv file
        try:
            remote = work.find('li', calss_='remote').text
            c_remote = " ".join(remote.split())
        except:
            c_remote = 'N/A'

        list = [c_title, c_salary, c_location, c_time, c_remote]
        writer.writerow(list)

#creating a csv for the function to store the datas
with open('reedjobs.csv', 'w', newline='') as f:
    writer = writer(f)
    header = ['Title', 'Location', 'Salary', 'Duration', 'Type']
    writer.writerow(header)

    logging.basicConfig(filename='reedjobs.log', level = logging.DEBUG,
                        format='%(asctime)s-%(message)s')

    html = urlopen('https://www.reed.co.uk/jobs/coding-jobs')
    bs = BeautifulSoup(html, 'html.parser')
    jobs =(bs.find_all('div', class_="col-sm-12 col-md-9 col-lg-9 details"))
    jobs_nr = int(len(jobs))

    #takes the line that has the number of jobs available from the html code
    total_pages = bs.find('div', class_ = 'page-counter' ).text

    #takes only the 'of (    ) 'jobs' text
    cut = re.compile('of\s[0-9],\d+\sjobs')

    #does the separating thingy
    n = (str(cut.findall(total_pages)))
    number = int(n[4:-6].replace(',' ,''))

    #result = the number of pages
    page_number = math.ceil(number / jobs_nr)

    #used to search throughout the jobs pages
    for i in range(0,page_number+1):
        pagejob(i)
