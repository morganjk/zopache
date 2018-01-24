#Subject to the CV License agreement.


from zope import interface
from zope.interface import Interface
from zope import schema
from zopache.crud.interfaces import *

#Views that are in the web menu. 
class IWeb(Interface):
      pass

class IHistoricDetails(Interface):
      pass

class ISource(Interface):      

    title = schema.TextLine(
        title = u'Version Name:',
        description = u'Describe this HTML Page.',
        required = False,
    )

    source= schema.Text(
        title = u'Source:',
        description = u'This is the text which defines the HTML.',
        required = False,
        default = u'',
    )



#NO DISPLAYALE, IT RETURNS SOME VERSION OF SOURCE
class ISourceLeaf(ISource,IRenameable,
            IDeletable):
      pass


class IHTML(ISourceLeaf):
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
