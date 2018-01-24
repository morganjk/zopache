from zope.interface import Interface
from pprint import pprint as pp 
from .css import ICSS
from .javascript import IJavascript
from .interfaces import ISource, IHTML
from . import tal_template
from zopache.core.page  import  Page
from dolmen.view import name, context, view_component
from cromlech.browser.directives import title
from dm.historical import getHistory
from crom import target, order
from cromdemo.interfaces import ITab
from zope.interface import implementer
from zopache.ttw.interfaces import IHistoricDetails
from cromlech import browser
from cromlech.browser.exceptions import HTTPFound

"""
#Maybe this is a much simpler versin for more recent zodb. 
def getHistory(item, size=40):
         db=item._p_jar.db()
         oid=item.__data._p_oid
         for version in db.history(oid,size):
             tid=version['tid']   #tid=the Transaction ID
             historicConnection= Connection(db,before=tid)
             historicObject=historicConnection.get(oid)
             yield historicObject
"""
@view_component
@name('history')
@title("History")
@target(ITab)
@context(Interface)
class History(Page):

       def results(self):
           return getHistory(self.context,last=200)

       def pp(self,item):
           return pp(item)
       template = tal_template('history.pt')

@view_component
@name('historicindex')
@title("Historic Index")
@target(ITab)
@context(ISource)
@implementer (IHistoricDetails)
class HistoricIndex(Page):
       def item(self):
           offset=self.request.form['offset']
           offset = int(offset)
           item= getHistory(self.context)[offset]['obj']
           return item

       def render(self ):  
           return self.item().source



@view_component
@name('historicview')
@title("Historic View")
@target(ITab)
@context(ISource)
@implementer (IHistoricDetails)
class HistoricView (HistoricIndex):
       def render(self ):  
           return self.item()(self)

@view_component
@name('restore')
@target(ITab)
@context(ISource)
@implementer (IHistoricDetails)
class Restore(HistoricIndex):
       def render(self ):  
           self.context.title=self.item().title
           self.context.source=self.item().source
           newURL=self.url(self.context)+'/aceEdit'
           raise HTTPFound(newURL)






