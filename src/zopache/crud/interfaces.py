# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import Interface, Attribute
from zope.schema import TextLine, Text, Object
from dolmen.container.interfaces import IBTreeContainer

#Views that are in the app menu.
#That menu is to be modified by users/developers. 
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

class IMoveable(Interface):
      pass

class ICopyable(Interface):
      pass

#Objects to which you can add stuff.  You cannot add stuff to leaves.  
class IAddContainer(Interface):
     pass

class IMoeabletale(Interface):
      pass

class ICopyable (Interface):
       pass

#Not HTML
class IContainer(
                 IBTreeContainer,
                 IAddContainer,
                 IRenameable,
                 ICopyable,
                 IDisplayable,
                 IDeletable,
                 IEditable
               ): 
     pass
 
class IImutable(     IBTreeContainer,
                     IAddContainer,
                     IDisplayable,
                     IEditable):
      pass

#The Root Container also has to implement IPublicationRoot      
#But you cannot delete or rename the root container
#So no IDeletable or IRenameable
class IRootContainer(IPublicationRoot,IImutable):
     pass

#You cannot add things to a leaf.    
class ILeaf(IRenameable,
            IDisplayable,
            IDeletable,
                 IMoveable,
                 ICopyable,
            IEditable):
      pass


