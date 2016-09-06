import database as db
import thorobred as tb
import sqlite3 as lite
import requests as r
import sys
import csv
import time
from random import randint

#grab random entries and most current place -> csv
con = lite.connect('TB.db')

with con:
	
	cur = con.cursor()
	cur.execute("SELECT * FROM HORSE ORDER BY RANDOM() LIMIT 50")

	rows = cur.fetchall()
	
	#myfile = open('50rand.csv','wb')
	#wr = csv.writer(myfile,quoting=csv.QUOTE_ALL)

	for row in rows:

		h_data = tb.lookup_horse(row[0])
		print "Horse: {}".format(h_data[0])

		cur.execute("SELECT ID FROM JOCKEY WHERE NAME='{}'".format(h_data[1]))
		jock = cur.fetchone()

		print "Jockey: {}  {}".format(jock[0], h_data[1])
		jockid=jock[0]
	#	time.sleep(3)
		jdata = tb.lookup_jock(jockid)	

		cur.execute("SELECT ID FROM TRAINER WHERE NAME='{}'".format(h_data[2]))
		train = cur.fetchone()

		
		print "Trainer: {}  {}".format(train[0], h_data[2])
		trainid=train[0]
	#	time.sleep(1)
		tdata = tb.lookup_train(trainid)


		data = []
		for x in h_data[4:-1]:
			data.append(int(x))
		for x in jdata[1:]:
			data.append(int(x))
		for x in tdata[1:]:
			data.append(int(x))

		data.append(int(h_data[-1]))	
		
		print "Data: {}".format(data)
		#wr.writerow(data)
	#	time.sleep(4)		
