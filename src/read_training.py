import csv

def read_race(filename, i):
	
	myfile = open(filename, 'r+')
	reader = csv.reader(myfile)

	num = 1
	entries = []

	for row in reader:

		#line only contains '-------' aka inbetween races
		if len(row) == 1:
			num = num+1

		if num == i:
			if len(row) > 3:
				#print row 
				entries.append(row)

	'''for horse in entries[0:]:
		for data in horse[1:]:
			data = int(data)'''
	
	return entries

