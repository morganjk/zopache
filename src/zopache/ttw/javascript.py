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
from dolmen.container import BTreeContainer

from zopache.ttw.interfaces import ISourceLeaf, ISourceContainer, IWeb

class IJavascript(ISource):
    "Basic Javascript Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this Javascript Object.',
        required = False,
    )

    source= schema.Text(
        title = u'Javascript',
        description = u'This is the text which defines the Javascriot.',
        required = False,
        default = u' ',
    )


class IJavascriptFolder(IJavascript, ISourceContainer):
    "Basic Javascript Folder Form"

@implementer(IJavascript)      
class Javascript(Leaf):
    source =u''
    className='Javascript'

    def getSource(self):
        return self.source

    def getTitle(self):
        return self.__name__

    def getJavascriptObjects(self):
         return [self]
 
    def getLines(self):
         result=self.source.replace(' ','mynbsp')
         result=cgi.escape(result)
         result=result.replace('mynbsp','&nbsp')
         return result.split("\n")

    def commands(self,view):
        manual=view.liHref(
            'http://www.zopache.com/baseicwebobjects/javascript',
             'Javascript Manual')
        return view.beginMenu('Javascript') + index  + edit + history + manual+ view.end 
                
    def __call__(self,view,**args):
            return self.getSource()

@implementer(IJavascriptFolder)
class JavascriptFolder(BTreeContainer):
    source =u''
    sourceCache=u''
    className='Javascript Folder'

    def commands(self,view):
        url=view.url(self)
        index=view.liHref(url+'/index','View')
        rawindex=view.liHref(url+'/rawindex','Raw')
        edit=view.liHref(url+'/edit','Edit')
        history=view.liHref(url+'/history','History')
        manage=view.liHref(url+'/list','Manage')
        search=view.liHref(url+'/manage','Search')
        addJavascriptFolder=view.liHref(url+'/addJavascriptFolder','Add Javascript Folder')
        addJavascript=view.liHref(url+'/addJavascript','Add Javascript')
        jsFolderCommands=(view.beginMenu('JSFolder') + 
                          index +
                          rawindex +
                          edit +
                          manage + 
                          search  + 
                          addJavascript +  
                          addJavascriptFolder +
                          view.end)
        return  jsFolderCommands

    def cacheSource(self):
        self.sourceCache=self.getSource()

    def getSource(self):
        if self.source!=None:
          result=self.source
        else:
          result=u' '  
        for item in self.values():
            result +=item.getSource()
        return result

    def getJavascriptObjects(self):
         result=[]
         for item in self.values():
             if IJavascript.providedBy(item):
                result+= item.getJavascriptObjects()
         return result

    def flatten(self,view):
         result=[]
         count=1
         class Record(object):
              pass
         objects=self.getJavascriptObjects()
         for anObject in objects:
             #JUST A LINE FOR THE FILE
             lines=anObject.getLines()
             o=Record()
             o.line=view.href(view.url(anObject)+'/edit', anObject.__name__)
             o.line="<h1>"+o.line+"</h1>"
             o.count=''
             result.append(o)

             for line in anObject.getLines():
                 o=Record()
                 o.line=line
                 o.count=view.href(view.url(anObject)+'/edit', str(count))
                 count=count+1
                 result.append(o)

         return result

from zopache.ttw.acescripts import AceScripts
class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/javascript");
        </script>
        """     

    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/javascript','Javascript Manual')
        return manual 

@form_component
@name('addJavascript')
@context(IBTreeContainer)
@target(ITab)
@title("Add Javascript")
@permissions('Manage')
@implementer(IWeb)
class AddJavascript(AceScripts,AddForm):
    interface = IJavascript
    ignoreContent = True
    factory=Javascript

@form_component
@name('addJavascriptFolder')
@context(IBTreeContainer)
@target(ITab)
@title("Add JavascriptFolder")
@permissions('Manage')
@implementer(IWeb)
class AddJavascriptFolder(AceScripts,AddForm):
    interface = IJavascriptFolder
    ignoreContent = True
    factory=JavascriptFolder    
    
                
"""
class EditJavascript(MyEditForm,Scripts):
    grok.template ("default_template_form")
    grok.require("zopache.Untrusted")
    grok.context(IJavascript)
    label = 'Edit Javascript Object'
    grok.name('edit')
    form_fields =  grok.AutoFields(IJavascript) 

    @grok.action('Edit Javascript Object')
    def edit(self, **data):
        self.applyData(self.context, **data)
        self.createJavascriptCaches()    
        self.status=u'Javascript Was Edited'
     
    def createJavascriptCaches(self):
        parentJavascriptFolders=parentsWhichImplement(self.context,IJavascriptFolder)
        # YOU MAY WANT TO IMPROVE THIS BY USING THE JSMIN LIBRARY
        for folder in parentJavascriptFolders:
            folder.sourceCache=folder.getSource()


class ManageJavascript(EditJavascript):
     grok.context(IJavascript)
     grok.name('manage')

from zopache.zmi.folder import Manage as ManageFolder
class ManageJavascriptFolder(ManageFolder):
     grok.context(IJavascriptFolder)
     grok.name('list')

class EditJavascriptFolder(EditJavascript):
     grok.context(IJavascriptFolder)

class ZopacheView(grok.View):
    grok.baseclass()
    def setDisplayObject(self,anObject):       
               self.zopacheTemplate=anObject


    def getTheObject(self):
            if hasattr(self,'zopacheTemplate'):
                 theObject=self.zopacheTemplate
            else:
                 theObject=self.context
            return theObject

class JavascriptIndex(ZopacheView):
       grok.context(IJavascript)
       grok.name('index')
       
       def render(self ):
            self.response.setHeader('Content-Type', 
                          u'application/javascript') 
            theObject=self.getTheObject()
            if IJavascriptFolder.providedBy(theObject):
                   return theObject.sourceCache
            else: 
                   return theObject.source               

class RawIndex(ZopacheView):
       grok.context(IJavascript)
       grok.name('rawindex')
       
       def render(self ):
            self.response.setHeader('Content-Type', 
                          u'application/javascript') 
            theObject=self.getTheObject()
            if IJavascriptFolder.providedBy(self.context):
                   return theObject.getSource()
            else: 
                   return theObject.source               




from zopache.zmi.breadcrumbs import Breadcrumbs
class SearchJavascriptFolder(grok.View,Breadcrumbs):
       grok.require("zopache.History")
       grok.context(IJavascriptFolder)
       grok.template ("javascriptFolder")
       grok.name('manage')
       label="Search Javascript Folder"
       className='Javacript Folder'
       

"""    



