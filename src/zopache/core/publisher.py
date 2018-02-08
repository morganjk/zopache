import dawnlight
from cromlech.dawnlight import DawnlightPublisher
from  zopache.core.traverser import Traverser
from cromlech.dawnlight.utils import safeguard
from cromlech.browser import IPublisher, IView, IResponseFactory
from zope.interface.interfaces import ComponentLookupError
from zopache.ttw.historyitem import HistoryTraverser

from cromlech.dawnlight.publish import shortcuts, PublicationError

class Publisher (DawnlightPublisher):
    """Traverses model objects, and looks up views. 
    """
    def __init__(self,view_locator):
         self.view_locator=view_locator
   
    @safeguard
    def publish(self, request, root,handle_errors):
        view=None
        path = self.base_path(request)
        crumbs = dawnlight.parse_path(path, shortcuts)
        traverser=Traverser(self.view_locator)
        context=root

        while crumbs:
           aType, name=crumbs.popleft()
           if (aType =='history'):
              # CALL THE HISTORY TRAVERSER
              print ("Historic Item  " , name, context.__name__)
              historyTraverser=HistoryTraverser(context,None)
              context=historyTraverser.traverse('history',name)
              continue
           context, view =traverser(context,request,name)
           if view != None:
                    break

        #If that did not work  check for a default view
        if view is  None:
           name=u'index'
           searchOn=('default','index')        
           context, view=traverser.checkForDefaultView(context,request,name)

        if view is None:                
           searchOn=('default','index')
           name='index'
           context, view=traverser.checkForTemplateAndView(
                  context,request,name)           
        
        #IF A VIEW WAS FOUND, RETURN IT 
        if (view is  not None):
                    factory = IResponseFactory(view)
                    return factory()

        raise PublicationError('%r can not be rendered.' % context)                
