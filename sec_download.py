# Download and analyze 10Q/10k filings form different companies


#from SECEdgar.crawler import SecCrawler
#seccrawler = SecCrawler()
#seccrawler.filing_10K('AAPL','0000320193','200010101','10')
import requests
import re
from bs4 import BeautifulSoup

def downloadfile(ftpfolder,filename):
    from ftplib import FTP
    ftp = FTP('ftp.sec.gov')
    ftp.login()
    ftp.cwd(ftpfolder)
    ##TODO : Generate folder structure based on company form type and append to local file name form name and year qtr..
    localfile = open('intel.xls','wb')
    #list =  ftp.dir()
    try:
        ftp.retrbinary('RETR ' + filename ,localfile.write, 1024 )
    except:
        # unable to handle this error.. program exits upon hitting file open error.. follow up !@#@!
        print  ' File error: File may be open ? '
    ##   print i
    localfile.close()
    ftp.quit()

# TODO
# Write function to find subfolder on the fly
# Get cik or company name on the fly and match to cik

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
    soup = BeautifulSoup(page1.text,"html.parser")
    #print soup.prettify()[0:1000]
    tables = soup.find("table", summary="Results")
    #th = tables.find_all('th', text='Filings')
    for row in tables.find_all("tr"):
        #print row
        #cells = row.find_all("td")
        for cells in row.find_all("td"):
            print cells
            print type(cells)
            print len(cells)
            # filingtype = cells[0].find(text=True)
            # format =  cells[1].find(text = True)
            # descrip = cells[2].find(text=True)
             # filedate = cells[3].find(text=True)
             # print filedate
                      
    print type(soup)
    print type(tables)
    #print filedate
    #print tables
    

    return newurl

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

ticker = raw_input('Enter the Stock ticker')
onecik = ciklookup(ticker)
print onecik
form = '10-q'
priortodate = '20010101'
totalcount = '100'
folderpath = folderlookup(ticker,form,priortodate,totalcount)
print "folderpath"

#onecik = ciklookup(ticker)
#cik = stripzero(onecik)
#print 'CIK of ticker %s is %s' %(ticker,cik)
#ftpfolder = generate_ftp_folder()


#filename = 'Financial_Report.xlsx'
#print '----------------------------------'
#print list
#downloadfile(ftpfolder,filename)



