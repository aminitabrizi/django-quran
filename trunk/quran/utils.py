from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import simplejson

def render_response(req, *args, **kwargs):
    if req.is_ajax():
        import pdb; pdb.set_trace()
        return HttpResponse(simplejson.dumps(args[1]['form']), mimetype='application/json')

    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)
    
from django.http import HttpResponse, HttpResponseRedirect
def http_redirect(req, url):
    if req.is_ajax():
        msg = {'next': url}
        return HttpResponse(simplejson.dumps(msg), mimetype='application/json')
    else:
        return HttpResponseRedirect(url)

# from http://www.djangosnippets.org/snippets/369/		
import re
import unicodedata
from htmlentitydefs import name2codepoint
from django.utils.encoding import smart_unicode, force_unicode

def slugify(s, entities=True, decimal=True, hexadecimal=True, instance=None, slug_field='slug', filter_dict=None):
    s = smart_unicode(s)

    #character entity reference
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

    #decimal character reference
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass

    #hexadecimal character reference
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass

    #translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

    #replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())

    #remove redundant -
    s = re.sub('-{2,}', '-', s).strip('-')

    slug = s
    if instance:
        def get_query():
            query = instance.__class__.objects.filter(**{slug_field: slug})
            if filter_dict:
                query = query.filter(**filter_dict)
            if instance.pk:
                query = query.exclude(pk=instance.pk)
            return query
        counter = 1
        while get_query():
            slug = "%s-%s" % (s, counter)
            counter += 1
    return slug
