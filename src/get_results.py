from lxml import html
import requests as r
import json
from datetime import datetime

#loop through this month at a given track and print outcomes into a csv
#with '----' as a seporator
#this program looks up the results from the past month from a given track and returns 
#all races in an array

result_URL = 'http://www.equibase.com/static/chart/summary/tracktimeUSA-EQB.html?SAP=views1'

month = datetime.now().month
if month < 10:
	month = '0{}'.format(month)
year = str(datetime.now().year)
s_year = year[-2:]

time = '{}x{}'.format(month,s_year)

URL = result_URL.replace('time',time)

#AT THIS TIME LEAVING OUT POST NUMBERS
def get_results(track):

	result_list = []
	total = 1
	res_URL = URL.replace('track', track)
	#time needs to be 0month0daylast2digitofyear
	#loop through current month to get results
	for i in xrange(1,30):

		if i < 10:
			x = "0{}".format(i)	
		else:
			x = "{}".format(i)

		url = res_URL.replace('x',x)
		page = r.get(url)
		tree = html.fromstring(page.content)

		if page.status_code == 200:
			#print url
			#top 3 results table: race1 = [2], race2 =[4], race5 =[10]
			#race info aka type: race1 = [1], race2 = [6], race3 = [11]
			#add 5 to each
			#others div starts at [3] and then add five for the next race

			info = '//html/body/div[1]/section[4]/div[2]/div[1]/div[x]'
			results='//html/body/div[1]/section[4]/div[2]/div[1]/table[x]/tbody'
			others = '//html/body/div[1]/section[4]/div[2]/div[1]/div[x]/'

			#count up to find result div and others div
			r_count = 1
			o_count = 3
			for y in range(1,13):

				current_race = []

				skip = False

				#ty(pe), res(ults), ot(hers)
				ty = info.replace('x',str(r_count))
				res = results.replace('x',str(y*2))	
				ot = others.replace('x',str(o_count))
				
				race_info = tree.xpath(ty+'/text()')
				others_info = tree.xpath(ot+'/a/text()')
				others_post = tree.xpath(ot+'text()')

				other_horses = []
				other_post = []

				for x in race_info:
					if x.find('Maiden') != -1:
						skip = True
			
				if skip == False:
					race_num = y
					date = '{}-{}-{}'.format(month,i,year)
					first = tree.xpath(res+'/tr[2]/td[2]/a/text()')

					if first:
						f_post = tree.xpath(res+'/tr[2]/td[1]/div/text()')
				
						one = "{} {}".format(f_post, first)
						second = tree.xpath(res+'/tr[3]/td[2]/a/text()')
						s_post = tree.xpath(res+'/tr[3]/td[1]/div/text()')
					
						two = "{} {}".format(s_post, second)

						third = tree.xpath(res+'/tr[4]/td[2]/a/text()')
						t_post = tree.xpath(res+'/tr[4]/td[1]/div/text()')			
						three = "{} {}".format(t_post, third)

						#need to find the rest
				
						for z in others_info:
							if z.find('\r\n\t\t\t\t\t\t') != -1:
								other_horses.append(z.replace('\r\n\t\t\t\t\t\t',""))

						#if race exists because first was found	
						print "{}  {}  {}   {}".format(track, date, race_num, total)
						#print "{}\n{}\n{}".format(first[0],second[0],third[0])
						
						current_race.extend([track, date, race_num])
						current_race.extend([first[0], second[0], third[0]])
						for x in range(len(other_horses)):
							#print "{} ".format(other_horses[x])
							current_race.extend([other_horses[x]])

			
						result_list.append(current_race)
						print "\n"	
						total = total+1
				
				r_count = r_count + 5
				o_count = o_count + 5
			print "----------"
	return result_list

