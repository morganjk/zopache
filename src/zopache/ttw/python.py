#This software is subject to the CV License Agreement.

from dolmen.forms.base import Actions
from zopache.crud import actions as formactions, i18n as _
from zopache.crud.actions import AddAction,EditAction
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
from RestrictedPython import compile_restricted_function
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.interfaces import ISourceLeaf

class IPython(ISourceLeaf):
    """Basic CSS FORM with CRUD"""
    title = schema.TextLine(
        title = u'Title',
        description = u'A short reminder of what this Python code  does or its version name.',
        required = False,
    )

    testURL = schema.TextLine(
        title = u'Test URL',
        description = u'URL To Visit to test this script',
        required = False,
    )
    
    source= schema.Text(
        title = u'Python SOurce Code',
        description = u'The Python code goes here.',
        required = False,
        default = u'',
    )



    
    
@implementer(IPython)
class Python(Leaf):

    def commands(self,view):
        url=view.url(self)
        index=view.liHref(url+'/index','View')
        manual=view.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return index + manual 

    #We could compile it when loaded from the ZODB
    def getCode(self):
       if not hasattr(self,'_v_code'):
          self.compileAndSavePython()
       return self._v_code

    def justCompilePython(self,code):
        return compile_restricted_function('', self.source, self.__name__)        
    def compileAndJavePython(self):
        compiled=compile_restricted_function('', self.source, self.__name__)
        self.saveResults(compiled)

    def saveResults(self,compiled):
        self._v_code=compiled.code
        self._v_errors=compiled.errors
        self._v_warnings=compiled.warnings
        #Not yet needed, but someone may want the following
        #self._v_used_names=compiled.used_names
        safe_locals = {}
        safe_globals = (safe_builtins +
                        limited_builtins +
                        utility_builtins)
        exec(compiled.code, safe_globals, safe_locals)
        self._v_compiled_function = safe_locals['function_name']

    def __call__(self,*k1, **kw2):
        return self.getCode(*kw1, **kw2)
    

class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/python");
        </script>
        """

class ValidatePython(object):    
         def validate(self):
             self.parentClass.validate(self)
             newCode=self.request.POST.get('form.field.source')
             result=self.context.compile(newCode)
             if result._v_errors != None:
                 raise ValidationError()
             if self._v_warnings != None:
                 raise ValidationError()             
             self.errors="Failed"
             
class AddPythonAndEdit(ValidatePython,AddAction):
    parentClass=AddAction
    def newURL(self,baseURL):
        return baseURL + '/ckedit'

class AddPythonAndTest(ValidatePython,AddAction):
    def newURL(self,baseURL):
        return self.form.context.testURL

class EditPython (ValidatePython, EditAction):
    parentClass=EditAction
    def newURL(self,baseURL):
        return baseURL + '/ckedit'
    
class EditPythonAndTest(ValidatePython,EditAction):
    def newURL(self,baseURL):
        return self.form.context.testURL        
    
@form_component
@name('addPython')
@context(IBTreeContainer)
#@target(ITab)
@title("Add Python")
@permissions('Manage')
@implementer(IWeb)
class AddPython(AceScripts,AceAddForm):
    label = "Add  a Python  Object"
    interface = IPython
    ignoreContent = True
    factory=Python
    
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    
    
    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return manual 
    @CachedProperty
    def actions(self):
        return Actions(
              AddPythonAndEdit(_("Add and Edit","Add -> Edit"), self.factory),
              AddPythonAndTest(_("Add and Test","Add -> AceEdit"), self.factory),
              formactions.CancelAction(_("Cancel","Cancel")))


def make_python_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/python'
        return response    

@form_component
@context(IPython)
@target(ITab)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditPython(AceScripts,AceEditForm):
    label = "Edit a Python Object"
    def footerScripts(self):
        return AceScripts.footerScripts(self)

    def headerScripts(self):
          return AceScripts.headerScripts(self)    

    @CachedProperty
    def actions(self):

        action1=EditPython("Save","Save")
        action2=EditPythonAndTest("Save  and View","Save -> View")
        action3=formactions.CancelAction("Cancel","Cancel")
        return Actions(action1,action2,action3)


@form_component
@context(IPython)
@target(ITab)
@name('manage')
@implementer(IWeb)
@title("Manage")
@permissions('Manage')
class ManagePython(AceEditPython):    
   pass
