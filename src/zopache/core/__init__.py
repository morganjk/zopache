#This is a package. 
from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("zopache.core")
from cromlech.browser.interfaces import IPublicationRoot
from os import path
from dolmen.template import TALTemplate
from dolmen.view import View, make_layout_response
from cromlech.webob.response import Response

from cromlech.container.contained import Contained
from persistent import Persistent
from cromlech.location import get_absolute_url


class Leaf(Contained, Persistent):
    pass


TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')
def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))

class Page(View):
        responseFactory = Response
        make_response = make_layout_response

        def url(self):
           return get_absolute_url(self.context, self.request)
                        
from cromlech.browser.interfaces import IPublicationRoot                        
def getRoot(object):
        max = 9999
        context=object
        while context is not None:
            if IPublicationRoot.providedBy(context):
                return context
            context = context.__parent__
            max -= 1
            if max < 1:
                raise TypeError("Maximum location depth exceeded, "                                "probably due to a a location cycle.")
        raise TypeError("Parents needed to  determine location root")

def title_or_name(obj):
    title = getattr(obj, 'title', None)
    if title is not None:
        return title
    return getattr(obj, '__name__', u'')
