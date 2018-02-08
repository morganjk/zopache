#Subject to the Zope and CV Licesnse

# SO HERE WE HAVE A CUSTOM TRAVERSER.
# IT TRAVERSES TO THE OBJECT AND LOOKS UP THE VIEW
# IT ALSO HANDLES CASES WHERE THE TEMPLATE IS LOOKED UP IN THE PARENTS
# SO IT IS A LITTLE BIT TRICKY, BUT MINIMAL ADAPTATION
# MAKES IT EASIER TO UNSERSTAND
from zope.interface.interfaces import ComponentLookupError
from zopache.ttw.acquisition import Acquire
from copy import copy 
from dolmen.container import IBTreeContainer

class Traverser(object):
    def __init__(self,view_lookup):
        self.view_lookup=view_lookup
        self.zopacheTemplate = None

    def __call__(self,context,request,name):
        
        #TRAVERSE THE CONTAINER
        if IBTreeContainer.providedBy(context):
            item = context.get(name,None)
            if item != None:
                print ("Traersed Container " , context.__name__ , item.__name__)#
                return item, None
            else:
               print ("Not indexing container", context.__name__)         

        #NOW CHECK FOR A VIEW ON A THE FINAL NODE
        try:
           view = self.view_lookup(request, context, name)
           if view is not None:
              return context, view
        except:
             view=None
        return context, None

    def checkForDefaultView(self,context,request,name):
        #NOW CHECK FOR A VIEW ON A THE FINAL NODE
        try:
            view = self.view_lookup(request, context, name)
        except ComponentLookupError:
            view=None        
        return context, view

    def checkForTemplateAndView(self,context,request,name):           
        # LOOK UP THE TEMPLATE, STORE IT, RETURN the LAST KNOWN OBJECT
        item=Acquire(context)[name]
        if item == None:
                print("Did not find a template")
                raise NotFound(self.context, name, request)
        # WE HAVE A STORED TEMPLATE
        else:
            zopacheTemplate=item
            view = self.view_lookup(request, zopacheTemplate, name)            
            if view is not None:
              if hasattr(view, 'setDisplayObject'):
                view.setDisplayObject(zopacheTemplate)           
                view.context=context  
                print ("View on template " , name)
                return context, view
              else:
                 print ("Not displaying THe View for A Template ", zopacheTemplate.__name__)

        
        """
        #THE FOLLOWING CODE IS NOT USED        
        #THE CASE WHERE THE TEMPLATE WAS ACQUIRED
        zopacheTemplate=self.zopacheTemplate
        if zopacheTemplate is not None:
           view = self.view_lookup(request, zopacheTemplate, name)
           if view is not None:
                view.setDisplayObject(zopacheTemplate)           
                view.context=context  
                print ("View on TEMPLATE  Context=  " ,
                       zopacheTemplate.__name__,
                       context.__name__)
                return context, view
           else:
              print ("Not displaying a template")
              

        #NOW CHECK FOR A VIEW ON A LEAF
        view = self.view_lookup(request, context, name)
        if view is not None:
            # FouND THE VIEW FOR A LEAF -1 TEMPLATE
            if hasattr(view, 'setDisplayObject'):
              print ("View  on context " , name,context.__name__)
              view.setDisplayObject(self.context)           
              return context, view
            else:
              # FouND THE VIEW FOR A REGULAR OBJECT
              return context, view              
        else: #THERE IS NO VIEW
            print ("Not displaying a view for a leaf", context.__name_)                      
        """
