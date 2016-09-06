import get_results
import sqlite3 as lite
import csv
import thorobred as tb
import sys

filename = sys.argv[1]
con = lite.connect('TB.db')

myfile = open(filename, 'wb')
wr = csv.writer(myfile,quoting=csv.QUOTE_ALL)

#church hill downs and gulfstream park last month
CD_results = get_results.get_results('CD')
GP_results = get_results.get_results('GP')
AP_results = get_results.get_results('AP')
PIM_results = get_results.get_results('PIM')

cur = con.cursor()

#do the same for other results
def write_train(results):

	for race in results:
		
		date = race[1].split('-')

		#writes track date race number	
		cur.execute('SELECT ID FROM HORSE WHERE NAME="{}"'.format(race[3]))
		x = cur.fetchone()	

		if x:
			skip = False
			print "{} {}".format(x[0], race[3])	
			wr.writerow(race[:3])

			for horse in race[3:]:
				cur.execute('SELECT ID FROM HORSE WHERE NAME="{}"'.format(horse))
				try:
					h_id = cur.fetchone()[0]
					h_data = tb.lookup_horse(h_id)
				except:
					skip = True
				
				cur.execute('SELECT ID FROM JOCKEY WHERE NAME="{}"'.format(h_data[1]))
				try:
					j_id = cur.fetchone()[0]
					j_data = tb.lookup_jock(j_id)
				except:
					skip = True


				cur.execute('SELECT ID FROM TRAINER WHERE NAME="{}"'.format(h_data[2]))
				
				try:
					t_id = cur.fetchone()[0]
					t_data = tb.lookup_train(t_id)
				except:
					skip = True

				second_date = h_data[-4]#[0].split('-')
				second_date = second_date.split('-')

				if h_data[-3][0] != 'D':
					second_finish = int(h_data[-3][0])

				else:
					second_date = 0

				last_date = h_data[-2].split('-')
	
				if h_data[-1][0] != 'D':
					last_finish = int(h_data[-1][0])

					
				else:
					last_finish = 0

	
				print "SECOND DATE {}\n".format(second_date)
				print "LAST DATE {} \n".format(last_date)
	
				starts = 0
				FIRST = 0
				SECOND = 0
				THIRD = 0	

				if second_date:
					if int(date[0]) == int(second_date[0]):

						if int(date[1]) <= int(second_date[1]):
							starts = 2
							if second_finish == 1:
								FIRST = FIRST +1

							if second_finish == 2:
								SECOND = SECOND +1

							if second_finish == 3:
								THIRD = THIRD +1

							#if int(date[0]) < int(last_date[0]):	
							if last_finish == 1:
								FIRST = FIRST +1

							if last_finish == 2:
								SECOND = SECOND +1

							if last_finish == 3:
								THIRD = THIRD +1
				
				elif int(date[0]) == int(last_date[0]):
				
					if int(date[1]) <= int(last_date[1]):

						print "IN HERE!!!!!!!!!!!!!"
						starts = 1

						if last_finish == 1:
							FIRST = FIRST +1

						if last_finish == 2:
							SECOND = SECOND +1

						if last_finish == 3:
							THIRD = THIRD +1


				data = []

				if not skip:
			
					h_data[4] = str(int(h_data[4]) - starts)
					h_data[5] = str(int(h_data[5]) - FIRST)
					h_data[6] = str(int(h_data[6]) - SECOND)
					h_data[7] = str(int(h_data[7]) - THIRD)

					data.append(h_data[0])	
					for x in h_data[4:-4]:
						data.append(int(x))
					for x in j_data[1:]:
						data.append(int(x))
					for x in t_data[1:]:
						data.append(int(x))


	
				#wr.writerow([str(horse)])
					wr.writerow(data)
			wr.writerow(['-------------------------'])
			#myfile.close()
		else:
			print "DIDNT FIND HORSE IN TABLE"




write_train(CD_results)
write_train(GP_results)
write_train(AP_results)
write_train(PIM_results)
