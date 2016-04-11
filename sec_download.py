# Download and analyze 10Q/10k filings form different companies


#from SECEdgar.crawler import SecCrawler
#seccrawler = SecCrawler()
#seccrawler.filing_10K('AAPL','0000320193','200010101','10')
import requests
import re
import datetime
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
from bs4 import BeautifulSoup

def downloadfile(ftpfolder,ftpfilename,localname):
    from ftplib import FTP
    ftp = FTP('ftp.sec.gov')
    ftp.login()
    logger.info ('Changing to ftp path %s',ftpfolder)
    ftp.cwd(ftpfolder)
    ##TODO : Generate folder structure based on company form type and append to local file name form name and year qtr..
    localfile = open(localname,'wb')
    #list =  ftp.dir()
    try:
        ftp.retrbinary('RETR ' + ftpfilename ,localfile.write, 1024 )
    except:
        # unable to handle this error.. program exits upon hitting file open error.. follow up !@#@!
        print  ' File error: File  %s does not exist in FTP path %s',ftpfilename,ftpfolder
    ##   print i
    localfile.close()
    ftp.quit()

# TODO
# Write function to find subfolder on the fly..Done
# Get cik or company name on the fly and match to cik ..DONE
# Write a function that can retrieve all the filenames from ftp path 
# Modify the download function so that it can download all Excel(xlsx or xls ) or text documents or all documents (you will have to do this one by one..)

# Extract ftp folder path/cik everything straigh from the search results and extracting from the table for results....
# https://www.sec.gov/cgi-bin/browse-edgar?CIK=intc&owner=exclude&action=getcompany&Find=Search
#https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000050863&type=10-q&dateb=20010101&owner=exclude&count=100

def folderlookup(ticker,formtype,date,count):
    newurl = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+ticker+'&type='+formtype+'&dateb='+date+'&owner=exclude&count='+count
    print newurl
    try:
        page1 = requests.get(newurl)
    except:
        print "unable to retrieve URL. URL or server error"
    soup = BeautifulSoup(page1.text,"lxml") #trying lxml as per bs recommendation
    tables = soup.find('table',summary='Results')
    tr = tables.find_all('tr')
    ftp_path = []
    filedate = []
    formtype = []
    for tr in tables.find_all('tr'):
        td = tr.find_all('td')
        if td: # checking so we can skip first header row..
            formtype.append(td[0].text)
            raw_loc =  td[1].a["href"]   ## beautiful soup returns a list and we need to access the individual elements of the list so we can operate on them using bs objects such as.string etc.
            extract_loc = re.findall('/edgar/data(/[0-9]+/[0-9]+)',raw_loc) #extracting the path usign regular expressino from second element.. this will return a list and need to extract..
            if extract_loc: #only if the regular expression is a match
                ftp_path.append(extract_loc[0]) # then append to path
            filedate.append(td[3].text)
    return formtype,filedate,ftp_path

def ciklookup(ticker):
    URL = 'https://www.sec.gov/cgi-bin/browse-edgar?CIK='+ticker+'&owner=exclude&action=getcompany&Find=Search'
    page = requests.get(URL)
    ciks = re.findall('CIK=([0-9]+)',page.text)
    cik_internal = ciks[0]   # getting all the cik using findall can be  cut short to stop at first if needed
    return cik_internal

def generate_ftp_folder(): #creating the path to travers sec.gov ftp site using the index
    folder = '000005086315000072' ## TODO make this generic next
    ftpfolderpath = '/' + cik + '/' + folder 
    return ftpfolderpath
    
def stripzero(cikzero): # removes the leading zero from CIK for the purpose of navigation into ftp folder
    cik_int = re.findall('([1-9][0-9]+)',cikzero)
    return str(cik_int[0])

ticker = raw_input('Enter the Stock ticker:')
form = raw_input('Enter Form  Type eg. 10-q /10-k...:')
today = datetime.date.today()
todaysdate = str(today.year)+str(today.month)+str(today.day) #converting to str and then concatenating
priortodate = todaysdate
totalcount = '100'
form,dates,path = folderlookup(ticker,form,priortodate,totalcount)  #form type , file date, ftp navigation path

filename = 'Financial_Report.xlsx'
print '----------------------------------'

for i in range(len(form)):
    logger.info('%s %s %s',form[i],dates[i],path[i])
    if form[i] == '10-K/A':
        form[i] = '10-K_A'    # / breaks windows file naming conventions.. changing to underscore
    localfilename = ticker+'_'+form[i]+'_'+dates[i]+'.xlsx' #generating the file name to store locally 
    downloadfile(str(path[i]),filename,localfilename)






