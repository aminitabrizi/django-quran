from django.contrib import admin
from models import quran, translation, surah

class translation_inline(admin.TabularInline):
	model = translation
	extra = 0

class quran_admin(admin.ModelAdmin):
	ordering = ['id',]
	list_display = ('surah_num', 'ayat_num')
	fieldsets = [
		(None, { 'fields' : ['surah_num', 'ayat_num']}),
	]
	inlines = [translation_inline,]

class surah_admin(admin.ModelAdmin):
	ordering = ['surah_num',]
	list_display = ('surah_num', 'surah_slug', 'surah_name')

#class quran_inline(admin.TabularInline):
#	model = quran
#	extra = 0

class translation_admin(admin.ModelAdmin):
	ordering = ['id',]
	list_display = ( 'surah_ayat', 'text')

	def surah_ayat(self, obj):
		try:
			qobj = quran.objects.get(pk=obj.quran_s_id)
		except quran.DoesNotExist:
			return '0:0'
		return '%s:%s' %(qobj.surah_num, qobj.ayat_num)
	surah_ayat.short_description = 'Surah:Ayat Number'
	#inlines = [quran_inline,]

admin.site.register(quran, quran_admin)
admin.site.register(translation, translation_admin)
admin.site.register(surah, surah_admin)

