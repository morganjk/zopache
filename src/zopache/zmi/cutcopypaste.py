##############################################################################
#
# Copyright (c) 2001, 2002 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Copy, Paste and Move support for content components
"""
__docformat__ = 'restructuredtext'

import crom
from zope.interface import implementer, Invalid
from zopache.copy import copy
from zope.interface import implementer
from zope.interface import Interface
from zopache.crud.interfaces import IRenameable,IDeletable,ICopyable
from zopache.crud.interfaces import IMoveable 
from zopache.zmi.interfaces import IObjectCutter
from zopache.zmi.interfaces import IObjectDeleter
from zopache.zmi.interfaces import IObjectCopier
from zopache.zmi.interfaces import IObjectRenamer
from zopache.zmi.interfaces import IObjectPaster

from dolmen.container.interfaces import IBTreeContainer#, IOrderedContainer
from .utilities import pasteFolder
from zopache.crud.utilities import uniqueName

class BaseClass(object):
    def __init__(self, object):
        self.context = object
        self.__parent__ = object # TODO: see if we can automate this
        
    def uniqueName(self,target, new_name):
        return uniqueName(target, new_name)

    def moveFrom(self,firstFolder,firstName, secondFolder, secondName):
        obj=firstFolder[firstName]
        del firstFolder [firstName]
        secondFolder[secondName] = obj

@crom.adapter
@crom.sources(Interface)
@crom.target(IObjectCutter)
class Cutter(BaseClass):
    """Adapter for moving objects between containers
    """

    def cut(self,view):
        self.view = view        
        """ Move the object to the pastefolder"""
        if not self.allowed():
                return
        obj=self.context    
        oldName=obj.__name__
        toFolder=pasteFolder(self)
        newName=self.uniqueName(toFolder,oldName)
        container = obj.__parent__
        self.moveFrom(container, oldName, toFolder, newName)        

    def allowed(self):
        if  IMoveable.providedBy(self.context):
                return True 
        return False

@crom.adapter
@crom.sources(Interface)
@crom.target(IObjectCopier)
class Copier(BaseClass):
    def copy(self,view):
        self.view = view        
        """ Move the object to the pastefolder"""
        obj=self.context
        if not self.allowed():
                return
        toFolder=pasteFolder(self)
        oldName=obj.__name__
        newName=self.uniqueName(toFolder,oldName)
        toFolder[newName]= copy(obj)

        
    def allowed(self):
        obj=self.context
        if  ICopyable.providedBy(obj):
                return True 
        return False


@crom.adapter
@crom.sources(Interface)
@crom.target(IObjectPaster)
class Paster(BaseClass):
                           
    def paste(self,view):
        self.view = view        
        """Copy this object to the `target` given.
        """
        toContainer = self.context
        fromFolder=pasteFolder(self)
        
        #Modifying a BTree while iterating over it does not work. 
        items=[]
        for item in fromFolder.values():                   
            items.append(item)
        for item in items:    
           orig_name = item.__name__
           new_name=self.uniqueName(toContainer,orig_name)
           if not self.allowed(item):
               self.view.error +=orig_name + " NOT PASTED"
               continue 
           self.moveFrom(fromFolder, orig_name, toContainer, new_name)

    def allowed(self,obj):
        if  ICopyable.providedBy(obj):
                return True
        return False

@crom.adapter
@crom.sources(Interface)
@crom.target(IObjectRenamer)
class Renamer(BaseClass):
    def renameItem(self, oldName, newName,view):
        self.view = view
        container=self.context
        obj = container.get(oldName)
        if obj is None:
            raise ItemNotFoundError(self.container, oldName)
        if not self.allowed():
                     return
        new_name=self.uniqueName(container,newName)
        self.moveFrom(container,oldName, container, newName)                

    def allowed(self):
        if  IRenameable.providedBy(self.context):
                return True
        return False

#THIS IS THE GENERIC DELETER
# JUST DELETE THE OBJECT
@crom.adapter
@crom.sources(Interface)
@crom.target(IObjectDeleter)
class Deleter(BaseClass):
    def deleteItem(self,view):
        self.view = view
        obj=self.context
        container=obj.__parent__
        if not self.allowed():
            self.view.error +=  name + " was not deleted. <br>"
            return
        name=obj.__name__
        del container[name]

    def allowed(self):
        if  IDeletable.providedBy(self.context):
                return True
        return False
