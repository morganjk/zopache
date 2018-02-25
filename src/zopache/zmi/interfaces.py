import crom
from zope.interface import Interface
from dolmen.container import IBTreeContainer

class IURLSegment(Interface):
    pass


@crom.adapter
@crom.sources(Interface)
@crom.target(IURLSegment)
class IEditAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'edit'

@crom.adapter
@crom.sources(IAceEdit)
@crom.target(IURLSegment)
class IAceEditAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'aceedit'


@crom.adapter
@crom.sources(ICkEdit)
@crom.target(IURLSegment)
class ICkEditAdaptor(object):
    def __init__(self,context):
        self.context=context   
    def getSegment(self):
        return 'ckedit'        
    
@crom.adapter
@crom.sources(IBTreeContainer)
@crom.target(IURLSegment)
class IManageAdaptor(object):
    def __init__(self,context):
        self.context=context
    def getSegment(self):
        return 'manage'    



class IObjectCutter(Interface):
     pass

class IObjectCopier(Interface):
     pass

class IObjectDeleter(Interface):
     pass

class IObjectRenamer(Interface):
     pass

class IObjectPaster(Interface):
     pass
