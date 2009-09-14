from django import template
from quran.models import quran, translation, surah, translation_info

register = template.Library()

def do_ayat(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, surah_num, ayat_num, translator = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a three argument" % token.contents.split()[0]
    # if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
        # raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return AyatNode(surah_num, ayat_num, translator)

class AyatNode(template.Node):
	def __init__(self, surah_num, ayat_num, translator):
		self.surah_num = template.Variable(surah_num)
		self.ayat_num = template.Variable(ayat_num)
		self.translator = template.Variable(translator)
	def render(self, context):
		try:
			qobj = quran.objects.get(surah_num = self.surah_num.resolve(context), ayat_num = self.ayat_num.resolve(context))
		except quran.DoesNotExist:
			return ''

		try:
			tiobj = translation_info.objects.get(tr_slug__exact = self.translator.resolve(context))
		except translation_info.DoesNotExist:
			return ''
			
		trobj = translation.objects.filter(quran_s__exact = qobj.id, trans_info_s__exact = tiobj.id)
		if trobj.count() == 0:
			return ''

		return trobj[0].text

register.tag('quran_ayat', do_ayat)
