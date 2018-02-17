#Subject to the CV License agreement.


from zope import interface
from zope.interface import Interface
from zope import schema
from zopache.crud.interfaces import *
from zopache.core.interfaces import ISource, IHTML
from zopache.core.interfaces import IAceHTML, ICkHTML
from zopache.crud.interfaces import ILeaf

class ITestURL(Interface):    
    testURL = schema.TextLine(
        title = u'Test URL',
        description = u'URL To Visit to test this script',
        required = False,
        default='/',            
    )

#Views that are in the web menu. 
class IWeb(Interface):
      pass

class IHistoryItem(Interface):
      pass

class IHistoricDetails(Interface):
      pass


#NO DISPLAYALE, IT RETURNS SOME VERSION OF SOURCE
class ISourceLeaf(ISource,ILeaf):
      pass

class IIndexHTML(Interface):
      pass


#THIS IS NOT ONLY HTML, IT IS THE HTML CLASS
#HAS TO DO WITH TRAVERSAL, AHD LOOKING UP THE VIEW

class IHTMLClass(IAceHTML,ICkHTML, IIndexHTML,ILeaf):
    pass

class IAceHTMLClass(IAceHTML, IIndexHTML,ILeaf):
    pass

  
#A COUNTAINER WITHOUT DISPLAYABLE
# RETURNS SOME VERSION OF SOURCE
#THIS IS USED BY JAVASCRIPT CONTAINERS
#AND HTML CONTAINERS
class ISourceContainer(ISource,
                    IBTreeContainer,
                    IAddContainer,
                    IRenameable,
                    ICopyable,
                    IMoveable,
                    IDeletable
               ): 
     pass

class IHTMLContainer(IHTML,ISourceContainer):
   pass


#This file is copied from my production servers.
#The stuff after this line is not yet needed for the
#pulic zopache release. 
"""

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
