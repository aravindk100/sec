import matplotlib.pyplot as plt
import sqlite3


conn = sqlite3.connect('secfinance.sqlite')
cur = conn.cursor()

valuetype = 1
plotlist = []
datelist = []
cur.execute('''SELECT * FROM summary WHERE valuetype_id=?''',(valuetype,))
for entry in cur.fetchall():
    print entry
    datelist.append(entry[2])
    plotlist.append(entry[3])


#expand to other rows in income sheet


plt.bar(datelist,plotlist,color="red",linestyle='-',linewidth=5)
plt.show()
