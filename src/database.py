import sqlite3 as sql

conn = sql.connect('TB.db')

print "Opened database successfully!"



def create_db():

	#eventually need training data, which entries will contain all stats
	#after looking up all data on trainers/jockies/horses

	conn.execute('''CREATE TABLE ENTRIES(
				ID INT PRIMARY KEY NOT NULL,
				NAME TEXT NOT NULL,
				JOCKEY TEXT NOT NULL,
				TRAINER TEXT NOT NULL,
				OWNER TEXT NOT NULL,
				Y_STARTS INT NOT NULL,
				Y_FIRSTS INT NOT NULL,
				Y_SECONDS INT NOT NULL,
				Y_THIRDS INT NOT NULL,
				Y_SPEED INT NOT NULL,
				C_STARTS INT NOT NULL,
				C_FIRSTS INT NOT NULL,
				C_SECONDS INT NOT NULL,
				C_THIRDS INT NOT NULL,
				C_SPEED INT NOT NULL);''')

	conn.execute('''CREATE TABLE HORSE(
					  ID INT PRIMARY KEY NOT NULL,
					  NAME TEXT NOT NULL);''')

	conn.execute('''CREATE TABLE JOCKEY(
					  ID INT PRIMARY KEY NOT NULL,
					  NAME TEXT NOT NULL,
					  NICK TEXT NOT NULL);''')

	conn.execute('''CREATE TABLE TRAINER(
					   ID INT PRIMARY KEY NOT NULL,
						NAME TEXT NOT NULL,
						NICK TEXT NOT NULL);''')
	
	print "Horse Table created successfully."

def horse_insert(data):
	'''table - table name; data - array size 2, id, name'''
	cur = conn.cursor()
	print "Inserting: {}   {}".format(data[0],data[1])
	cur.execute('INSERT OR REPLACE INTO HORSE VALUES ({},"{}")'.format(data[0],data[1]))
	conn.commit()	

def jock_insert(data):
	'''table - table name; data - array size 2, id, name'''
	cur = conn.cursor()
	name = data[1]

	print "Inserting: {}   {}  {} ".format(data[0],data[1],data[2])
	cur.execute('INSERT OR REPLACE INTO JOCKEY VALUES ({},"{}","{}")'.format(data[0],data[1],data[2]))
	conn.commit()	

def train_insert(data):
	'''table - table name; data - array size 2, id, name'''
	cur = conn.cursor()
	print "Inserting: {}   {}  {}".format(data[0],data[1],data[2])
	cur.execute('INSERT OR REPLACE INTO TRAINER VALUES ({},"{}","{}")'.format(data[0],data[1],data[2]))
	conn.commit()	


