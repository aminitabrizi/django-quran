# Create your views here.
from quran.models import quran, translation, surah, translation_info
from utils import render_response, http_redirect
from django.http import Http404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

def show_ayat(request, surah_num, ayat_num, translator):
	try:
		qobj = quran.objects.get(surah_num = surah_num, ayat_num = ayat_num)
	except ObjectDoesNotExist:
		return HttpResponse('No quran object found')

	try:
		tiobj = translation_info.objects.get(tr_slug__exact = translator)
	except ObjectDoesNotExist:
		return HttpResponse('No translator object found')
		
	trobj = translation.objects.filter(quran_s__exact = qobj.id, trans_info_s__exact = tiobj.id)
	if trobj.count() == 0:
		return Http404

	return render_response(request, 'quran/ayat.html',{'ayat':trobj[0].text, 'surah_num':surah_num, 'ayat_num':ayat_num, 'translator':'arabic'})
