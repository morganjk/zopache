#Subject to the CV License agreement.


from zope import interface
from zope.interface import Interface
from zope import schema
from zopache.crud.interfaces import *
from zopache.core.interfaces import ISource

#Views that are in the web menu. 
class IWeb(Interface):
      pass

class IHistoryItem(Interface):
      pass

class IHistoricDetails(Interface):
      pass



#NO DISPLAYALE, IT RETURNS SOME VERSION OF SOURCE
class ISourceLeaf(ISource,
                  IRenameable,
                  IDeletable):
      pass



#THIS IS NOT ONLY HTML, IT IS THE HTML CLASS
#HAS TO DO WITH TRAVERSAL, AHD LOOKING UP THE VIEW

class IHTMLClass(IHTML, ILeaf):
    pass

  
#A COUNTAINER WITHOUT DISPLAYABLE
# RETURNS SOME VERSION OF SOURCE
class ISourceContainer(ISource,IBTreeContainer,
                 IAddContainer,
                 IRenameable,
                 IDeletable
               ): 
     pass


#This file is copied from my production servers.
#The stuff after this line is not yet needed for the
#pulic zopache release. 
"""
class IHTMLIndex(IHTML):
    pass

class ISimpleBranch(Interface):
    title = schema.TextLine(
        title = u'Title',
        description = u'Title for this Branch.',
        required = False,
    )



class ITTWPrincipalFolder(Interface):
    pass


class IUntrustedHTML(IHTML):
   pass


class IZopache(Interface):
    pass

"""
