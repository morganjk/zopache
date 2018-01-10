# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute
from zope.schema import TextLine, Text, Object

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
class IAddale(Interface):
     pass
 
#You can do all of the above to a container.
class IContainer(IAddable, IRenameable, IDisplayable, IDeletable, IEditable): 
     pass

#The Root Container also has to implement IPublicationRoot      
#But you cannot delete or rename the root container
#So no IDeleteable or IRenameable
class IRootContainer(IBtreeContainer,IAddable,  IDisplayable,  IEditable):):        
     pass

#You cannot add things to a leaf.    
class ILeaf(IRenameable, IDisplayable, IDeletable, IEditable):
      pass
        
