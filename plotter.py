import matplotlib.pyplot as plt
import sqlite3
import datetime


conn = sqlite3.connect('secfinance.sqlite')
cur = conn.cursor()

valid = []
valtypname = []

cur.execute('''SELECT * FROM valuetype''')
for valtyp in cur.fetchall(): #getting all vallues i.e. netrevenue,netincome etc.
    print valtyp
    valid.append(valtyp[0])  #used for val id
    valtypname.append(valtyp[1]) # used for name of val type to include in label

plotlist = []
datelist = []
for index,valcount in enumerate(valid):
    cur.execute('''SELECT * FROM summary WHERE valuetype_id=?''',(valcount,)) #instead of passing 1 find the valuetype and its primary key at run time
    for entry in cur.fetchall():
        dateformat = datetime.datetime.strptime(entry[2], '%Y-%m-%d').date()
        datelist.append(dateformat)
        plotlist.append(entry[3])
    plt.plot_date(datelist,plotlist, fmt='bo', tz=None, xdate=True, ydate=False, ls='solid')
    plt.title(valtypname[index])
    #plt.bar(datelist,plotlist,color="red",linestyle='-',linewidth=5)
    plotlist = []
    datelist = []
    plt.show()
#expand to other rows in income sheet

