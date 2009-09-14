from django.db import models
from utils import slugify

# class ComboField(models.Field):
	# def __init__(self, *args, **kwargs):
		# self.col1 = kwargs['col1']
		# self.col2 = kwargs['col2']
		# super(ComboField, self).__init__(*args, **kwargs)

class quran(models.Model):
	surah_num = models.IntegerField(db_index = True, verbose_name = 'Surah Number')
	ayat_num = models.IntegerField(verbose_name = 'Ayat Number')

	# def __unicode__(self):
		# return '%s:%s' %(self.surah_num, self.ayat_num)

class translation_info(models.Model):
	author = models.CharField(max_length=50, verbose_name= 'Translation Author')
	tr_slug = models.SlugField(editable = False)

	def save(self):
		if not self.id:
			self.tr_slug = slugify(self.author, slug_field = 'tr_slug')
		super(translation_info, self).save()
		
class translation(models.Model):
	text = models.TextField()
	quran_s = models.ForeignKey(quran)
	trans_info_s = models.ForeignKey(translation_info)

class surah(models.Model):
	surah_name = models.CharField(max_length = 50, verbose_name = 'Surah Name')
	surah_num = models.IntegerField(verbose_name = 'Surah Number')
	surah_slug = models.SlugField(editable = False)

	def __unicode__(self):
		return self.surah_name
		
	def save(self):
		if not self.id:
			self.surah_slug = slugify(self.surah_name, instance=self, slug_field = 'surah_slug')
		super(surah, self).save()