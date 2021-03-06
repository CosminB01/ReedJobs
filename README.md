# ReedJobsTest
This repository presents a scraper that scrapes all the jobs from https://www.reed.co.uk/jobs/coding-jobs

## Development 

Install Python, if you don't have it:
  1. Start by updating the package list using the following command:
      > Sudo apt update
  2. Use the following command to install pip for Python 3:
  This command will also install all the dependencies required for building Python modules.
  
      > sudo apt install Python3-pip
	
Install BeautifulSoup4:
1. Because the BeautifulSoup library is not a default Python library, it must be installed
    > pip3 install BeautifulSoup4
    
## Steps

  1. Import your needed libraries:
  
> from urllib.request import urlopen

> from bs4 import BeautifulSoup

> import logging

> import re

> import math

> from csv import writer

  2. Build your function that will run the block of code that is parsing the job pages:
     
    def pagejob(pageURL):
    html = urlopen('https://www.reed.co.uk/jobs/coding-jobs?pageno={}'.format(pageURL))
    bs = BeautifulSoup(html, 'html.parser')
    soup = bs.find_all('div', class_='col-sm-12 col-md-9 col-lg-9 details')
    list = []
    for work in soup:
        #tries to get the title and if it isn't found, replaces the title with an error string that is shown in the log file
        try:
            title_ = work.find('h3', class_='title').text
        except:
            title_ = "cannot extract job's title - text not found"

        afterTitle = "Extracted job\'s title, value: "
        logging.info(afterTitle + title_)


        #tries to get the title and if it isn't found, replaces the title with an error string that is shown in the csv file
        try:
            title = work.find('h3', class_='title').text
            c_title = " ".join(title.split())
        except:
            c_title = 'N/A'


        #tries to get the salary and if it isn't found, replaces the salary with an error string that is shown in the log file
        try:
            salary_ = work.find('li', class_='salary').text
        except:
            salary_ = 'cannot extract job salary - text not found'
        afterSalary = "Extracted job\'s salary, value: "
        logging.info(afterSalary + salary_)


        # tries to get the salary and if it isn't found, replaces the salary with an error string that is shown in the csv file
        try:
            salary = work.find('li', class_='salary').text
            c_salary = " ".join(salary.split())
        except:
            c_salary = 'N/A'


        # tries to get the location and if it isn't found, replaces the location with an error string that is shown in the log file
        try:
            location_ = work.find('li', class_='location').text
        except:
            location_ = 'cannot extract job location - text not found'
        afterLocation = "Extracted job\'s location, value: "
        logging.info(afterLocation + location_)


        # tries to get the location and if it isn't found, replaces the location with an error string that is shown in the csv file
        try:
            location = work.find('li', class_='location').text
            c_location = " ".join(location.split())
        except:
            c_location = 'N/A'


        # tries to get the time of the job and if it isn't found, replaces the time of the job with an error string that is shown in the log file
        try:
            time_ = work.find('li', class_='time').text
        except:
            time_ = "cannot extract job duration - text not found"
        afterTime = 'Extracted job\'s duration, value: '
        logging.info(afterTime + time_)


        # tries to get the time of the job and if it isn't found, replaces the time of the job with an error string that is shown in the csv file
        try:
            time = work.find('li', class_='time').text
            c_time = " ".join(time.split())
        except:
            c_time = "N/A"


        # tries to get the type of the job(remote\site) and if it isn't found, replaces the type of the job(remote\site)
        # with an error string that is shown in the log file
        try:
            remote_ = work.find('li', calss_='remote').text
        except:
            remote_ = 'cannot extract job type - text not found'
        afterRemote = 'Extracted job\'s type, value: '
        logging.info(afterRemote + remote_)


        # tries to get the type of the job(remote\site) and if it isn't found, replaces the type of the job(remote\site)
        # with an error string that is shown in the csv file
        try:
            remote = work.find('li', calss_='remote').text
            c_remote = " ".join(remote.split())
        except:
            c_remote = 'N/A'

        list = [c_title, c_salary, c_location, c_time, c_remote]
        writer.writerow(list)
        
        
 This block of code will be executed when the function will be called and it'll go throught the page ***trying*** to get every job's title, salary, location, the working type (full-time, etc.) and see if it is remote or not. After that the code stores all the datas collected in a list that will be used in the ***csv*** file to store the found informations. Also the scraped informations from each job's detail (title, salary, location, etc.) are stored in a log.
 
   3. Creating a csv to store the informations found:
   
   			 	with open('reedjobs.csv', 'w', newline='') as f:
    		writer = writer(f)
    		header = ['Title', 'Location', 'Salary', 'Duration', 'Type']
    		writer.writerow(header) 
	
   4. Creating the log file:
   
   			logging.basicConfig(filename='reedjobs.log', level = logging.DEBUG,
                        		format='%(asctime)s-%(message)s')
				

   5. Finding out how many jobs are on the first page:
   
   			html = urlopen('https://www.reed.co.uk/jobs/coding-jobs')
    		bs = BeautifulSoup(html, 'html.parser')
    		jobs =(bs.find_all('div', class_="col-sm-12 col-md-9 col-lg-9 details"))
    		jobs_nr = int(len(jobs))
		
   6. Now we have to extract from the page the total number of jobs available(this will get all the text, e.g. 10 out of 2000, so we need only the '2000'- we'll get it in the next step):
   
   			total_pages = bs.find('div', class_ = 'page-counter' ).text
		
   7. Separating the wanted number form the rest of the words and numbers:

			n = (str(cut.findall(total_pages)))
    		number = int(n[4:11].replace(',' ,''))
		
   8. Now we need to find out the total number of pages so we know how to tell our scraper how much he has to dig :) :
   
   			page_number = math.ceil(number / jobs_nr)
    
   9. The final part is to do the for: that will tell the scraper what the range of scraping is:

   			for i in range(0,page_number+1):
        		pagejob(i)
	
	


