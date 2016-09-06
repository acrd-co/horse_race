import json
from lxml import html
import requests as r
import time #sleep some functions 
import numbers #check types
import re

top_TBhorse_url = 'http://www.equibase.com/Data.cfm/Stats/Horse/Year/Page?year=2016&page=1&sort=EARNINGS&dir=A&list=N&category=A&attribute_total=1024&set=full&race_breed_type=TB'


top_TBjock_url ='http://www.equibase.com/Data.cfm/Stats/Jockey/Year/Page?year=2016&list=N&sort=EARNINGS&dir=A&page=1&set=full&attribute_total=1024&race_breed_type=TB'


top_TBtrain_url ='http://www.equibase.com/Data.cfm/Stats/Trainer/Year/Page?year=2016&list=N&sort=EARNINGS&dir=A&page=1&set=full&attribute_total=1024&race_breed_type=TB'

top_TBown_url = 0 ##TODO ##might not be needed 


#these functions grab horse, jockey, and trainer info from the top 
#thoroghbred rankings up to a certain page number starting from the first


#function gets and returns Horse info from horse listing site
#include name, refno, starts, wins, show, place, win %
#refno will be used to look up profile later
#'referenceNumber'

def get_horses(start,end):

	pages = {}
		
	for x in xrange(start,end):
		url = top_TBhorse_url.replace('page=1', 'page={0}'.format(x+1))
		page = r.get(url)
		print '\nrequesting horse data...\n'
		j = json.loads(page.text)
		if not j['stats']:
			print "Horse data not found."
			break
		pages[x] = j
		print '\nsuccsesfully loaded page {} into json\n'.format(x+1)
		'''	print '-------------------------------'
		print '----------PAGE {0}-------------'.format(x+1)
		print '-------------------------------' '''
		#for y in j['stats']:
			#lookup_horse(y['referenceNumber'])

	return pages


def get_jocks(start, end):

	pages = {}	
	for x in xrange(start,end):
		url = top_TBjock_url.replace('page=1', 'page={0}'.format(x+1))
		page = r.get(url)
		print '\nrequesting jockey data...\n'
		j = json.loads(page.text)
		if not j['stats']:
			print "Jockey data not found."
			break
		pages[x] = j
		print '\nsuccsesfully loaded page {} into json\n'.format(x+1)

		'''	print '-------------------------------'
		print '----------PAGE {0}-------------'.format(x+1)
		print '-------------------------------'
		'''
		#for y in j['stats']:
			#print y['jockeyName'] 

		'''for y in j['stats']:
			print y['identity']
			lookup_jock(y['identity'])
			time.sleep(2)
		'''
	return pages	


def get_trains(start,end):

	pages = {}	
	for x in xrange(start,end):
		url = top_TBtrain_url.replace('page=1', 'page={0}'.format(x+1))
		page = r.get(url)
		print '\nrequesting trainer data...\n'
		j = json.loads(page.text)
		if not j['stats']:
			print "Trainer data not found."
			break
		pages[x] = j

		print '\nsuccsesfully loaded page {}  into json\n'.format(x+1)
		'''print '-------------------------------'
		print '----------PAGE {0}-------------'.format(x+1)
		print '-------------------------------' '''
		'''for y in j['stats']:
			print y['identity']
			lookup_train(y['identity'])
		'''
	return pages

def lookup_horse(refno):

	print "\nLooking up: " + str(refno)
	url = 'http://www.equibase.com/profiles/Results.cfm?type=Horse&refno=x&registry=T&rbt=TB'
	url = url.replace('x', str(refno))
	try:
		page = r.get(url,verify=False,timeout=10)
	except:
		time.sleep(5)
		return lookup_horse(refno)

	tree = html.fromstring(page.content)

	horsename = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[3]/div/div[2]/h2/strong/text()')

	if not horsename:
		horsename = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[3]/div/div[3]/h2/strong/text()')

	if not horsename:
		print "Horsename is empty. Probably a captcha."
		time.sleep(15)
		return lookup_horse(refno)
		'''x=raw_input("Fill it out (y/n): ")
		if x == 'y':
			return lookup_horse(refno)
		'''

	jockey = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[4]/div/div[1]/p[1]/a[1]/text()')

	trainer = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[4]/div/div[1]/p[1]/a[2]/text()')

	owner = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[4]/div/div[1]/p[1]/a[3]/text()')

	y_starts = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/table/tbody/tr[2]/td/text()')

	y_firsts = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/table/tbody/tr[3]/td/text()')

	y_seconds = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/table/tbody/tr[4]/td/text()')

	y_thirds = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/table/tbody/tr[5]/td/text()')

	y_speed = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[1]/table/tbody/tr[8]/td/text()')

	c_starts = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/table/tbody/tr[2]/td/text()')

	c_firsts = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/table/tbody/tr[3]/td/text()')

	c_seconds = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/table/tbody/tr[4]/td/text()')

	c_thirds = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/table/tbody/tr[5]/td/text()')

	c_speed = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[1]/div[1]/div[2]/table/tbody/tr[8]/td/text()')


	#most recent race track: eg Churchill Downs.. pimlico
	last_track = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[2]/div/table/tbody/tr[2]/td[1]/a/text()')

	if not last_track:
		last_track=tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[3]/div/table/tbody/tr[2]/td[1]/a/text()')

	#number of the race that given day
	last_race = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[2]/div/table/tbody/tr[2]/td[3]/text()')

	if not last_race:
		last_race=tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[3]/div/table/tbody/tr[2]/td[3]/text()')

	#short name for the track, easy to lookup
	last_nick = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[2]/div/table/tbody/tr[2]/td[1]/a/@href')

	if not last_nick:
		last_nick = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[3]/div/table/tbody/tr[2]/td[1]/a/@href')

	nick = last_nick[0]
	nick = nick.split('&')
	nick = nick[-2]
	nick = nick.replace('trk=', "")
	
	#date of the most recent race for the horse
	last_date = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[3]/div/table/tbody/tr[2]/td[2]/text()')

	if not last_date:
		last_date = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[2]/div/table/tbody/tr[2]/td[2]/text()')

	last_date = last_date[0]
	last_date = last_date.replace('/','-')
	
	last_finish = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[2]/div/table/tbody/tr[2]/td[6]/text()')

	if not last_finish:
		last_finish = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[3]/div/table/tbody/tr[2]/td[6]/text()')
		


	#second to most recent finish
	second_finish= tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[2]/div/table/tbody/tr[3]/td[6]/text()')

	if not second_finish:
		second_finish = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[3]/div/table/tbody/tr[3]/td[6]/text()')

		
	if second_finish == 'DNF':
		second_finish = '0'
	if last_finish == 'DNF':
		last_fniish = '0'
	#second to most recent date
	second_date = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[2]/div/table/tbody/tr[3]/td[2]/text()')
	
	if not second_date:
		second_date = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[5]/div[3]/div/table/tbody/tr[3]/td[2]/text()')


	second_date = second_date[0]
	second_date = second_date.replace('/','-')
		
	horsename = horsename[0].split('(')[0]
	jockey = jockey[0]
	trainer = trainer[0]
	y_starts = ((y_starts[0]).split(' '))[-1]
	y_firsts = ((y_firsts[0]).split(' '))[-1]
	y_seconds = ((y_seconds[0]).split(' '))[-1]
	y_thirds = ((y_thirds[0]).split(' '))[-1]
	y_speed = y_speed[1].replace(' ',"")
	c_starts = ((c_starts[0]).split(' '))[-1]
	c_firsts = ((c_firsts[0]).split(' '))[-1]
	c_seconds = ((c_seconds[0]).split(' '))[-1]
	c_thirds = ((c_thirds[0]).split(' '))[-1]
	c_speed = c_speed[1].replace(' ',"")
	second_finish = second_finish[0]
	last_finish = last_finish[0]
		
	print "Name: " + str(horsename)
	print "Jockey: " + str(jockey)
	print "Trainer: " + str(trainer)
	print "Owner: " + str(owner)

	print "---This Year Stats---"
	print "Starts: "+str(y_starts)
	print "Firsts: " + str(y_firsts)
	print "Seconds: "+ str(y_seconds)
	print "Thirds: " + str(y_thirds)
	print "Speed: " +  str(y_speed)
	print "--------------------"

	print "---Career Stats---"
	print "Starts: " + str(c_starts)
	print "Firsts: " + str(c_firsts)
	print "Seconds: "+ str(c_seconds)
	print "Thrids: " + str(c_thirds)
	print "Speed: " +  str(c_speed)
	print "URL: " +str(url)
	print "--------------------"
	print "Last track: "+str(last_track)
	print "Nick: "+str(nick)
	print "Second date: "+str(second_date)
	print "Second finish: "+str(second_finish)
	print "Last race #: "+str(last_race)
	print "Last date: "+str(last_date)
	print "Last finish: "+str(last_finish)
	print "-------------------\n"
		
	x=[horsename,jockey,trainer,owner,y_starts,y_firsts,y_seconds,y_thirds,y_speed,c_starts,c_firsts,c_seconds,c_thirds,c_speed,second_date,second_finish,last_date,last_finish]

	return x	

def lookup_jock(refno):

	print "\nLooking up: {}".format(refno)

	url = 'http://www.equibase.com/profiles/Results.cfm?type=People&searchType=J&eID=x&rbt=TB'

	url = url.replace('x', str(refno))

	try:
		page = r.get(url,verify=False,timeout=10)
	except:
		time.sleep(5)
		return lookup_jock(refno)

	string = (page.content).split('<')
	tree = html.fromstring(page.content)

	jockname = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[1]/div[2]/h2/strong/text()')
	
	if not jockname:
		jockname = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[1]/div[3]/h2/strong/text()')


	if not jockname:
		print "Jockname is empty. Probably a captcha."
		time.sleep(15)
		return lookup_jock(refno)
		'''x=raw_input("Fill it out (y/n): ")
		if x == 'y':
			return lookup_jock(refno)
		'''
	y_starts = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/table/tbody/tr[2]/td/text()')


	y_firsts = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/table/tbody/tr[3]/td/text()')

	y_seconds = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/table/tbody/tr[4]/td/text()')

	y_thirds = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/table/tbody/tr[5]/td/text()')


	#:TODO: career stats: not sure why these arent working??????

	
	for s in string:
		if "Starts" in s:
			curr = s.split()
			num = curr[-1].replace(",","")
			try:
				num = int(num)
				c_starts=['Starts: {}'.format(num)]			
			except:
				pass	

	
		if "Firsts" in s:
			curr = s.split()
			num = curr[-1].replace(",","")
			try:
				num = int(num)
				c_firsts=['Firsts: {}'.format(num)]			
			except:
				pass	

		if "Seconds" in s:
			curr = s.split()
			num = curr[-1].replace(",","")
			try:
				num = int(num)
				c_seconds=['Seconds: {}'.format(num)]			
			except:
				pass	

		if "Thirds" in s:
			curr = s.split()
			num = curr[-1].replace(",","")
			try:
				num = int(num)
				c_thirds=['Thirds: {}'.format(num)]			
			except:
				pass	

	print "Jockname: {}".format(jockname)
	jockname = jockname[0]
	y_starts = ((y_starts[0]).split(' '))[-1]
	y_firsts = ((y_firsts[0]).split(' '))[-1]
	y_seconds = ((y_seconds[0]).split(' '))[-1]
	y_thirds = ((y_thirds[0]).split(' '))[-1]
	c_starts = ((c_starts[0]).split(' '))[-1]
	c_firsts = ((c_firsts[0]).split(' '))[-1]
	c_seconds = ((c_seconds[0]).split(' '))[-1]
	c_thirds = ((c_thirds[0]).split(' '))[-1]

	print "Name: " + str(jockname)
	print "---This Year Stats---"
	print "Starts: " + str(y_starts)
	print "Firsts: " + str(y_firsts)
	print "Seconds: "+ str(y_seconds)
	print "Thrids: " + str(y_thirds)
	print "--------------------"
	print "---Career Stats---"
	print "Starts: " + str(c_starts)
	print "Firsts: " + str(c_firsts)
	print "Seconds: "+ str(c_seconds)
	print "Thrids: " + str(c_thirds)
	print "------------------\n"

	x=[jockname,y_starts,y_firsts,y_seconds,
		y_thirds,c_starts,c_firsts,c_seconds,c_thirds]
	return x	

	

def lookup_train(refno):

	print "Looking up: {}".format(refno)

	url = 'http://www.equibase.com/profiles/Results.cfm?type=People&searchType=T&eID=x&rbt=TB'

	url = url.replace('x', str(refno))
	
	try:
		page = r.get(url,verify=False,timeout=10)
	except:
		time.sleep(5)
		return lookup_train(refno)
	string = (page.content).split('<') #break html down into line by line
	tree = html.fromstring(page.content)

	trainname = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[1]/div[2]/h2/strong/text()')

	if not trainname:
		trainname = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[1]/div[3]/h2/strong/text()')


	if not trainname:
		print "Trainname is empty. Probably a captcha."
		time.sleep(15)
		return lookup_train(refno)
		'''x=raw_input("Fill it out (y/n): ")
		if x == 'y':
			return lookup_train(refno)
		'''

	

	y_starts = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/table/tbody/tr[2]/td/text()')

	y_firsts = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/table/tbody/tr[3]/td/text()')

	y_seconds = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/table/tbody/tr[4]/td/text()')

	y_thirds = tree.xpath('//html/body/div[1]/section[4]/div/div[2]/div[1]/div[2]/div[7]/div[1]/div[1]/div[1]/table/tbody/tr[5]/td/text()')


	#go through every html line until finding Starts/firsts/etc then 
	#break it down
	for s in string:
		if "Starts" in s:
			curr = s.split()
			num = curr[-1].replace(",","")
			try:
				num = int(num)
				c_starts=['Starts: {}'.format(num)]			
			except:
				pass


		if "Firsts" in s:
			curr = s.split()
			num = curr[-1].replace(",","")
			try:
				num = int(num)
				c_firsts=['Firsts: {}'.format(num)]			
			except:
				pass	

		if "Seconds" in s:
			curr = s.split()
			num = curr[-1].replace(",","")
			try:
				num = int(num)
				c_seconds=['Seconds: {}'.format(num)]			
			except:
				pass	

		if "Thirds" in s:
			curr = s.split()
			num = curr[-1].replace(",","")
			try:
				num = int(num)
				c_thirds=['Thirds: {}'.format(num)]			
			except:
				pass	

	trainname = trainname[0]
	y_starts = ((y_starts[0]).split(' '))[-1]
	y_firsts = ((y_firsts[0]).split(' '))[-1]
	y_seconds = ((y_seconds[0]).split(' '))[-1]
	y_thirds = ((y_thirds[0]).split(' '))[-1]
	c_starts = ((c_starts[0]).split(' '))[-1]
	c_firsts = ((c_firsts[0]).split(' '))[-1]
	c_seconds = ((c_seconds[0]).split(' '))[-1]
	c_thirds = ((c_thirds[0]).split(' '))[-1]


	
	print "Name: " + str(trainname)
	print "---This Year Stats---"
	print "Starts: " + str(y_starts)
	print "Firsts: " + str(y_firsts)
	print "Seconds: "+ str(y_seconds)
	print "Thrids: " + str(y_thirds)
	print "--------------------\n"
	
	print "---Career Stats---"
	print "Starts: " + str(c_starts)
	print "Firsts: " + str(c_firsts)
	print "Seconds: "+ str(c_seconds)
	print "Thrids: " + str(c_thirds)
	print "--------------------\n"

	x=[trainname,y_starts,y_firsts,y_seconds,
		y_thirds,c_starts,c_firsts,c_seconds,c_thirds]
	return x	


