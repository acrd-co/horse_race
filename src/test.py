import lxml as html
import requests as r
import json
import sys
import csv

#test file to grab pdf, dump into text file and read results. not needed.
'''
page = r.get("http://www1.drf.com/drfPDFChartRacesIndexAction.do?TRK=TDN&CTY=USA&DATE=20160618&RN=1")

pdffile = open('data.pdf','wb')
pdffile.write(page.content)
pdffile.close()
'''
