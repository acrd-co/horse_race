import itertools
import numpy as np
from scipy import stats
import pylab as pl
from sklearn import svm, linear_model, cross_validation
from sklearn.linear_model import SGDClassifier as SGDC
from sklearn.ensemble import GradientBoostingClassifier as GBC
import read_training as rt
import random
import ranksvm

i = 1
x = [] 


while i <= 371:
	print i
	x.append(rt.read_race('copy.csv', i))
	i = i + 1

'''i = 1
while i <=214:
	print i
	x.append(rt.read_race('copy2.csv',i))
	i = i+1
'''
print "SIZE OF X: {}".format(len(x))

for race in x:
	
	for horse in race[:2]:
		horse.append(1)
		#y.append(1)

	for horse in race[2:3]:
		horse.append(1)
		#y.append(-1)

	for horse in race[3:4]:
		horse.append(0)
	
	for horse in race[4:]:
		horse.append(0)

	#for horse in race:
		#horse = [int(x) for x in horse[1:]]
		#print horse
		#train.append(horse)
	#print "=-----------\n"


#X =np.array([[[int(stat) for stat in entry[1:-1]] for entry in entries] for entries in x])
#y = np.array([[entry[-1] for entry in entries] for entries in x])
#y = np.array([1]*len(X))
#X =np.array([[int(stat) for entries in x] for entry in entries for stat in entry[1:-1]])
'''for race in xrange(len(X)):
	if race % 2.0 != 0:
		np.random.shuffle(X[race])
		y[race] = 0
'''

X = []
rank = []
for race in x:
	random.shuffle(race)
	for horse in race:
		y = []
		for stat in horse[1:-1]:
			y.append(int(stat))
		rank.append(horse[-1])
		X.append(y)

print "X: {}\n\nrank: {}".format(X,rank)


clf = GBC(loss='exponential',n_estimators=1000, learning_rate=0.01, max_depth=30,random_state=0).fit(X[:-100],rank[:-100])

#clf = SGDC(loss='hinge', penalty='l2').fit(X[:-50],rank[:-50])

i = 1
correct = 0
total = 0
allcorrect = 0

while i <= 100:
	test = np.array(X[-i]).reshape(1,26)
	predict = clf.predict(test)[0]
	print "Prediction: {}".format(predict)
	print "Actual: {}".format(rank[-i])
	i = i + 1
	actual = rank[-i]	

	if predict == 1:
		total = total + 1
		if actual == 1:
			correct = correct + 1

	if predict == actual:
		allcorrect = allcorrect + 1
	
print "{} correct out of {} when place guess\n".format(correct, total)
print "Overall {} for {}".format(allcorrect, i)
print "Total predictions: {}\n".format(i)

#print "Score: {}".format(clf.score(test, rank[-100:]))
'''
print "LENGTH X: {}\nLENGTH Y: {}".format(len(X), len(rank))
cv = cross_validation.KFold(len(X), len(X[0]))
train, test = iter(cv).next()
Y = np.c_[rank, np.mod(np.arange(len(X)), 26)]

Y = np.array(Y)
X = np.array(X)
rank_svm = ranksvm.RankSVM().fit(X[train],Y[test])

print 'Performance of ranking ', rank_svm.score(X[test],y[test])
'''
