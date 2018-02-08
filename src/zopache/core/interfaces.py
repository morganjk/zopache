from zope import schema
from zope.interface import Interface, Attribute

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
class IIndexHTML(Interface):
      pass
  
class ICkHTML (ISource):
     pass

class IAceHTML(ISource): 
     pass

class IHTML (ICkHTML,IAceHTML,ISource):
      pass

 
