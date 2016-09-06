import database as db
import thorobred as t

#pages3 = t.get_trains(0,400)

def fill_horse(start, end):
	
	print "requesting pages..."
	pages = t.get_horses(start,end)
	print "inserting into Horse table"
	for y in pages:
		for x in pages[y]['stats']:
			data = [x['referenceNumber'], x['horseName']]
			db.horse_insert(data)
	print "done."

def fill_jock(start,end):

	print "requesting pages..."
	pages = t.get_jocks(start,end)
	print "inserting into Jockey table"
	for y in pages:
		for x in pages[y]['stats']:
			data = [x['identity'], x['jockeyName']]
			name = data[1].split()

			if name[-1] == "Jr." or name[-1] == "Sr.":
				for x in xrange(len(name[:-2])):
					name[x] = name[x][0]
			else:
				for x in xrange(len(name[:-1])):
					name[x] = name[x][0]
		
			nick = " ".join(name)	
			data.append(nick)	
			db.jock_insert(data)
	print "done."


def fill_train(start,end):

	print "requesting pages..."
	pages = t.get_trains(start,end) 
	print "inserting into Trainer table"
	for y in pages:
		for x in pages[y]['stats']:
			data = [x['identity'], x['trainerName']]
			name = data[1].split()

			if name[-1] == "Jr." or name[-1] == "Sr.":
				for x in xrange(len(name[:-2])):
					name[x] = name[x][0]
			else:
				for x in xrange(len(name[:-1])):
					name[x] = name[x][0]
		
			nick = " ".join(name)	
			data.append(nick)	
			db.train_insert(data)
	print "done."



fill_jock(0,400)
fill_train(0,400)
