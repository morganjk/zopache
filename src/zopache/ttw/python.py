#sheThis software is subject to the CV License Agreement
from zope.schema import ValidationError
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
from RestrictedPython import compile_restricted
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.interfaces import ISourceLeaf
from RestrictedPython import safe_builtins, utility_builtins, limited_builtins
from RestrictedPython import RestrictingNodeTransformer

class OwnRestrictingNodeTransformer(RestrictingNodeTransformer):
        pass

policy = OwnRestrictingNodeTransformer

policy_instance = OwnRestrictingNodeTransformer(
            errors=[],
            warnings=[],
            used_names=[]
        )

class IPython(ISourceLeaf):
    """Basic Python  FORM with CRUD"""
    arguments = schema.TextLine(
        title = u'Arguments',
        description = u'An optional comma separated list of arguments',
        default='',
        required = False,
    )    
    
    source= schema.Text(
        title = u'Python Source Code',
        description = u'The Python code goes here.',
        required = False,
        default = u'',
    )
    title = schema.TextLine(
        title = u'Title',
        description = u'A short reminder of what this Python code  does or its version name.',
        default='',            
        required = False,
    )

    testURL = schema.TextLine(
        title = u'Test URL',
        description = u'URL To Visit to test this script',
        required = False,
        default='/',            
    )


@implementer(IPython)
class PythonFunction(Leaf):

    def commands(self,view):
        url=view.url(self)
        index=view.liHref(url+'/index','View')
        manual=view.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return index + manual 

    #We could save some cycles and only compile this when loaded from the ZODB
    def getCode(self):
       if not hasattr(self,'_v_code'):
          self.compile()
       return self._v_compiledFunction

    def compile(self):
        compiled = compile_restricted_function(
            self.arguments,
            self.source,
            self.__name__)
        self._v_code=compiled.code
        self._v_errors=compiled.errors
        self._v_warnings=compiled.warnings
        #Not yet needed, but someone may want the following
        #self._v_used_names=compiled.used_names
        safe_locals = {}
        #safe_globals = (safe_builtins +
        #                limited_builtins +
        #                utility_builtins)
        
        exec(compiled.code, safe_builtins, safe_locals)
        self._v_compiledFunction = safe_locals[self.__name__]
    
    def __call__(self,*args, **kwargs):
        code=self.getCode()
        #Apparently templates always add **kwargs
        numberOfArguments=len(args)
        if (numberOfArguments ==0):
                return code()
        else:
                return code(args)
        #if (numberOfArguments ==2):
        #        return code(args[0])
        #if (numberOfArguments ==3):
        #        return code(args[0],args[1])
        #if (numberOfArguments ==4):
        #        return code(args[0],args[1],args[2])
        #if (numberOfArguments ==5):
        #        return code(args[0],args[1],args[2],args[3])


class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/python");
        </script>
        """

class ValidatePython(object):    
     def validateCore(self,form,name):
             self.parentClass.validate(self,form)
             new=PythonFunction()
             new.__name__=name
             new.source=form.request.POST.get('form.field.source')
             new.arguments=form.request.POST.get('form.field.arguments')
             result=new.compile()
             if len(new._v_errors) != 0:
                 import pdb; pdb.set_trace()
                 self.errors="Failed"
                 raise ValidationError()
             if len(new._v_warnings) != 0:
                 self.errors="Failed"
                 raise ValidationError()             
             return True
             
class AddPythonAndEdit(ValidatePython,AddAction):
    parentClass=AddAction
    def newURL(self,baseURL):
        return baseURL + '/ckedit'

class AddPythonAndTest(ValidatePython,AddAction):
    parentClass=AddAction
    def newURL(self,baseURL):
        return self.form.new.testURL

class EditPython (ValidatePython, EditAction):
    parentClass=EditAction
    def newURL(self,baseURL):
        return baseURL + '/ckedit'

    #Validate on Edit        
    def validate(self,form):
            self.form=form
            name=form.context.__name__
            return self.validateCore(form,name)


    
class EditPythonAndTest(EditPython):
    parentClass=EditAction
    def newURL(self,baseURL):
        return self.form.context.testURL        
    
@form_component
@name('addPythonFunction')
@context(IBTreeContainer)
#@target(ITab)
@title("Add Python")
@permissions('Manage')
@implementer(IWeb)
class AddPythonFunction(AceScripts,AceAddForm):
    label = "Add  a Python  Object"
    interface = IPython
    ignoreContent = True
    factory=PythonFunction
    
    def postProcess(self):
        self.new.compile()    

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
              AddPythonAndTest(_("Add and Test","Add -> Test"), self.factory),
              formactions.CancelAction(_("Cancel","Cancel")))

    #Validate on Add
    def validate(self,form):
            name=form.request.POST.get('form.field.__name__')
            return self.validateCore(form,name)
    

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
