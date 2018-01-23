from chameleon import PageTemplate
from zope import interface
from zope import schema
from zopache.ttw.acquisition import ParentalAcquire
from zope.schema.interfaces import IField
from zope.interface import Interface
from zopache.ttw.interfaces import ISource,IHTML
from zopache.crud.components import AddForm, EditForm
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
from dolmen.view import name, context, view_component

"""
HTML is a very important base class.  It has a field called source.  It 
can be edited witht the WYSIWYG ckEditor or the more technical Ace Editor.
So those are two different views of the class. 

The ckEditor by default strips out the <html><head> and <body> tags. 
That is great for a CMS, but for beginners might be better to leave it in. 

We can imagine multiple versions of the html class.  Trusted HTML  allows 
python scripts to be called.   Untrusted HTML does not. There could also 
be an TrustedHTMLContainer, and an UntrustedHTML Containers

""" 
class HTMLBase(Leaf):

    def __init__(self):
        self.source=' '

    def getTitle(self):
        if hasattr(self,'title') and self.title!= None and len(self.title)>0:
           return self.title
        else: 
           return 'Please edit the  Title'

    def getContext(self,view):
            if hasattr(view,'getContext'):
               context=view.getContext()
            else:
                context=view.context
            return context

@implementer(IHTML)
class TrustedHTML(HTMLBase):
    def setTemplate(self):
            if not hasattr(self,'_v_compiledTemplate'):
               self.compileTemplate()
            return self._v_compiledTemplate 

    def compileTemplate(self):
                 source=self.source
                 self._v_compiledTemplate = PageTemplate(source)
                 return self._v_compiledTemplate

    # I AM NOT QUITE SURE WHY I HAVE 3 DIFFERENT CALL FUCTIONS
    def __call__(self,view,**args):
            context=self.getContext(view)
            return self.callWithContext(view,context,**args)

    def callWithContext(self,view,context,**args):
            self.setTemplate()
            return self._v_compiledTemplate(
                           context=context,
                           request=view.request,
                           view=view,
                           **args)

    def callRecursive(self,view,context,template):
            self.setTemplate()
            return self._v_compiledTemplate(
                           view=view,
                           context=context,
                           template=template,
                           )


class AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/html");
        </script>
        """


class CkScripts(object):
    def  headerScripts(self):
        return """
<style>
.ck-editor__editable {
    min-height: 250px;
    }
    </style>

    <script src="https://cdn.ckeditor.com/ckeditor5/1.0.0-alpha.2/classic/ckeditor.js"></script>
        """ + AddForm.headerScripts(self)
    
    def  footerScripts(self):
        return """
<script>
ClassicEditor
        .create( document.querySelector( '#form-field-source' ) )
        .then( editor => {
    console.log( editor );
        } )
        .catch( error => {
    console.error( error );
        } );
    </script>

        """ 


@form_component
@name('addHTML')
@context(IBTreeContainer)
@target(ITab)
@title("Add HTML")
@permissions('Manage')
@implementer(IWeb)
class AddHTML(CkScripts,AddForm):
    interface = IHTML
    ignoreContent = True
    factory=TrustedHTML
    def footerScripts(self):
        return CkScripts.footerScripts(self)

    def headerScripts(self):
          return CkScripts.headerScripts(self)    

from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response

@view_component
@name('index')
@context(IHTML)
@title("View")
class Index(View):
    responseFactory = Response
    make_response = make_view_response

    def render(self):
        return self.context(self)

@form_component
@context(IHTML)
@target(ITab)
@title("AceEdit")
@name("aceEdit")
@permissions('Manage')
class AceditHTML(AceScripts,EditForm):
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    

    def postProcess(self):
        self.context.compileTemplate()            


@form_component
@context(IHTML)
@target(ITab)
@name('ckEdit')
@title("ckEdit")
@permissions('Manage')
class ckEditHTML(CkScripts,EditForm):
    def footerScripts(self):
        return CkScripts.footerScripts(self)

    def headerScripts(self):
          return CkScripts.headerScripts(self)    

    def postProcess(self):
        self.context.compileTemplate()



        
    
"""    
#FOR THE ZMI, THE DEFAULT MANAGE VIEW IS THE EDIT HTML VIEW.
class ManageHTML(EditCK):
    grok.require("zopache.editText")
    grok.name('manage')
    grok.require("zopache.editText")



class ViewSnippet(formlib.DisplayForm,Breadcrumbs):
       grok.context(IUntrustedHTML)
       grok.require("zopache.Untrusted")
       grok.name('snippet')
       form_fields=[]

       def _render_template(self ):
            top="<html><head></head><body>"
            middle=self.context.source
            bottom="</body></html>"
            return top+middle+bottom



"""        

"""
#This stuff is used in my production servers,
#but has not been ported over to here.


class UntrustedHTMLBase(HTMLBase):
    grok.implements(IUntrustedHTML,ISource)
    def setTemplate(self):
        pass

    def compileTemplate(self):
        pass

    def __call__(self,view,**args):
            return self.source

class UntrustedHTML(UntrustedHTMLBase):
    grok.implements(IUntrustedHTML,IHTMLIndex,ISource)



class AddUntrustedHTML(AceScripts,Add):
    grok.require("zopache.Untrusted")
    grok.context(IZopache)
    grok.name('addTTWHTML')
    label = 'Add an HTML  Page TTW'


    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/html','HTML  Manual')
        return manual


    def newClass(self):
       return TTWHTML()



class EditUntrustedHTML(BaseEdit,AceScripts):
    grok.context(IUntrustedHTML)
    grok.require("zopache.Untrusted")
    grok.template ("default_template_form")
    label = 'Edit HTML Object TTW.'
    grok.name('aceedit')

    def breadcrumbs(self):
       return self.breadcrumbsFor('/manage',3,1,False)

    @grok.action('Save ')
    def edit(self, **data):
        self.baseEdit(**data)
        self.context.setTemplate()

    @grok.action('Save And View')
    def saveAndView(self, **data):
        self.baseEdit(**data)
        self.context.setTemplate()
        return self.redirect(self.url(self.context)+'/index')

    @grok.action('Reset')
    def reset(self, **data):
        self.status='Content Reset'

 #       self.context.source=""
<html>
  <head>
  </head>
  <body>
    Hello World
  </body>
</html>
#        ""
        self.context.setTemplate()




class ManageUntrustedHTML(CkScripts,EditTTWHTML):
    grok.require("zopache.Untrusted")
    grok.name('manage')

#This is used to throw up a login form. 
class IndexSecure(Index):
       grok.context(IHTMLIndex)
       grok.require('privacv.login')
       grok.name('indexsecure')
"""
