# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import Interface, Attribute
from zope.schema import TextLine, Text, Object
from dolmen.container.interfaces import IBTreeContainer
from zopache.core.interfaces import ISource, IHTML

#Views that are in the web menu. 
class IWeb(Interface):
      pass

#Views that are in the app menu. 
class IApp(Interface):
      pass

class IName(Interface):
      __name__ = TextLine(
           title=(u"URL Segment Name (required)"),
           required=True,
           default=None)

#Objects which can be deleted.  You cannot delte the root object. 
class IDeletable(Interface):
      pass

#Objects which can be edited.  
class IEditable(Interface):
    pass

#Objects which can be displayed
class IDisplayable(Interface):
     pass

#Objects which can be renamed.  You cannot rename the root object. 
class IRenameable(Interface):
     pass

#Objects to which you can add stuff.  You cannot add stuff to leaves.  
class IAddContainer(Interface):
     pass

 
#You can do all of the above to a container.
class IContainer(IHTML,
                 IBTreeContainer,
                 IAddContainer,
                 IRenameable,
                 IDisplayable,
                 IDeletable,
                 IEditable
               ): 
     pass



#The Root Container also has to implement IPublicationRoot      
#But you cannot delete or rename the root container
#So no IDeletable or IRenameable
class IRootContainer(IPublicationRoot,
                     IWeb,
                     IHTML,
                     IBTreeContainer,
                     IAddContainer,
                     IDisplayable,
                     IEditable):        
     pass

#You cannot add things to a leaf.    
class ILeaf(IRenameable,
            IDisplayable,
            IDeletable,
            IEditable):
      pass


