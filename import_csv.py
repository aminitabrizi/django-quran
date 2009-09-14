#!/usr/bin/python
import csv
import sys
import os
#from django.db import models
from django.core.exceptions import ObjectDoesNotExist

sys.path.append(os.path.realpath(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from quran.models import quran, translation, translation_info, surah
	
if len(sys.argv) != 3:
	print "%s <csv file name> <translator>" % sys.argv[0]
	sys.exit(-1)

try:
	tr_info = translation_info.objects.get(author__exact = sys.argv[2] );
	if tr_info:
		print "Translation with this author already exists"
		sys.exit(-1)
except translation_info.DoesNotExist:
	pass


print "Translator not found"
tr_info = translation_info(author = sys.argv[2])
tr_info.save()



reader = csv.reader(open(sys.argv[1]), delimiter=',', quotechar='"')

#skip header
reader.next()

count = 0
for row in reader:
	#print ":".join(row)
	try:
		qobj = quran.objects.get(surah_num = int(row[1]), ayat_num = int(row[2]))
	except quran.DoesNotExist:
		print "No index found for surah:ayat = %d:%d" % (row[1], row[2])
		tr_info.delete()
		break

	#print progress
	if count % 100 == 0:
		print('.'),
		sys.stdout.flush()


	#print "%d:%d %s" % (qobj.surah_num, qobj.ayat_num, row[3])
	count += 1
		
	trobj = translation(quran_s = qobj, trans_info_s = tr_info, text = row[3])
	trobj.save()
		
		
print "Number of rows added = %d" % count

if count == 0:
	tr_info.delete()