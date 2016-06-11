import matplotlib.pyplot as plt
import sqlite3
import datetime


conn = sqlite3.connect('secfinance.sqlite')
cur = conn.cursor()

valid = []
valtypname = []

cur.execute('''SELECT * FROM valuetype''')
for valtyp in cur.fetchall():
    print valtyp
    valid.append(valtyp[0])
    valtypname.append(valtyp[1])

#valuetype = 1
plotlist = []
datelist = []
for valcount in valid:
    cur.execute('''SELECT * FROM summary WHERE valuetype_id=?''',(valcount,)) #instead of passing 1 find the valuetype and its primary key at run time
    for entry in cur.fetchall():
        dateformat = datetime.datetime.strptime(entry[2], '%Y-%m-%d').date()
        datelist.append(dateformat)
        plotlist.append(entry[3])
    plt.plot_date(datelist,plotlist, fmt='bo', tz=None, xdate=True, ydate=False, ls='solid')
    #plt.bar(datelist,plotlist,color="red",linestyle='-',linewidth=5)
    plt.show()
    plotlist = []
    datelist = []
    print valcount

#expand to other rows in income sheet

