#This software is subject to the CV License Agreement.

from dolmen.forms.base import Actions
from zopache.crud import actions as formactions, i18n as _
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zope.interface import implementer
from dolmen.forms.base import action, name, context, form_component
from dolmen.container import IBTreeContainer
from crom import target, order
from cromdemo.interfaces import ITab
from cromlech.browser.directives import title
from cromlech.security import permissions
from zopache.core import Leaf
from zopache.crud.interfaces import IWeb
from dolmen.view import name, context, view_component
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from zope.cachedescriptors.property import CachedProperty

from zopache.ttw.interfaces import ISourceLeaf

class ICSS(ISourceLeaf):
    """Basic CSS FORM with CRUD"""

    title = schema.TextLine(
        title = u'Title',
        description = u'A short reminder of what this CSS page does or its versin name.',
        required = False,
    )

    source= schema.Text(
        title = u'CSS',
        description = u'This is the text which defines the CSS.',
        required = False,
        default = u'',
    )



@implementer(ICSS)
class CSS(Leaf):

    def commands(self,view):
        url=view.url(self)
        index=view.liHref(url+'/index','View')
        manual=view.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return index + manual 
                

from zopache.ttw.acescripts import AceScripts
class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/css");
        </script>
        """
    

@form_component
@name('addCSS')
@context(IBTreeContainer)
#@target(ITab)
@title("Add CSS")
@permissions('Manage')
@implementer(IWeb)
class AddCSS(AceScripts,AceAddForm):
    implements=IWeb
    interface = ICSS
    ignoreContent = True
    factory=CSS
    
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    
    
    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return manual 


def make_css_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/css'
        return response    

@view_component
@name('index')
@context(ICSS)
@title("View CSS")
class Index(View):
    responseFactory = Response
    make_response = make_css_response
        
    def render(self):
               return self.context.source


@form_component
@context(ICSS)
@target(ITab)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditCSS(AceScripts,AceEditForm):
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    

    def postProcess(self):
        pass




@form_component
@context(ICSS)
@target(ITab)
@name('manage')
@implementer(IWeb)
@title("Manage")
@permissions('Manage')
class ManageCSS(AceEditCSS):    
   pass
