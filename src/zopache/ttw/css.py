from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ISource
from zopache.crud.components import AddForm
from zope.interface import implementer
from dolmen.forms.base import action, name, context, form_component
from dolmen.container import IBTreeContainer
from crom import target, order
from cromdemo.interfaces import ITab
from cromlech.browser.directives import title
from cromlech.security import permissions
from zopache.core import Leaf
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.interfaces import IWeb



from zopache.ttw.interfaces import ISourceLeaf

class ICSS(ISourceLeaf):
    """Basic CSS FORM with CRUD"""

    description = schema.TextLine(
        title = u'Description',
        description = u'A short reminder of what this CSS page does.',
        required = False,
    )

    source= schema.Text(
        title = u'CSS',
        description = u'This is the text which defines the CSS.',
        required = False,
        default = u'',
    )




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
@target(ITab)
@title("Add CSS")
@permissions('Manage')
@implementer(IWeb)
class AddHTML(AceScripts,AddForm):
    implements=IWeb
    interface = ICSS
    ignoreContent = True
    factory=CSS
    
    def footerScripts(self):
        return CkScripts.footerScripts(self)

    def headerScripts(self):
          return CkScripts.headerScripts(self)    
    
    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return manual 
     
"""
class Edit(MyEditForm,Breadcrumbs,Scripts):
    grok.template ("default_template_form")
    grok.require("zopache.Untrusted")
    formlib.context(ICSS)
    label = 'Edit CSS'
    form_fields =  grok.AutoFields(ICSS)
 
    @grok.action('Edit CSS')
    def edit(self, **data):
        self.applyData(self.context, **data)
        return self.redirect(self.url(self.context)+'/manage')



class Manage(Edit):
     pass


class Index(formlib.DisplayForm,Breadcrumbs):
       grok.context(ICSS)
       grok.require("zope.Public")
       form_fields=[]

       def _render_template(self ):
            self.response.setHeader('Content-Type', 
                          u'text/css') 
            return self.zopacheTemplate.source

       def setDisplayObject(self,anObject):       
               self.zopacheTemplate=anObject
       
"""
       



