# Download and analyze 10Q/10k filings form different companies


#from SECEdgar.crawler import SecCrawler
#seccrawler = SecCrawler()
#seccrawler.filing_10K('AAPL','0000320193','200010101','10')

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
def ciklookup(ticker):
    if ticker == 'intc':
        cik_internal = '50863'
    return cik_internal
 


def generate_ftp_folder():
    folder = '000005086315000072'
    ftpfolderpath = '/' + cik + '/' + folder 
    return ftpfolderpath

ticker = raw_input('Enter the Stock ticker')
cik = ciklookup(ticker)
ftpfolder = generate_ftp_folder()


filename = 'Financial_Report.xlsx'
print '----------------------------------'
print list
downloadfile(ftpfolder,filename)




