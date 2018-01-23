from dm.historical import getHistory, getObjectAt
from pprint import pprint as pp 
from interfaces import ISource
from css import ICSS
from javascript import IJavascript
from interfaces import ISource, IHTML
from . import tal_template
from zopache.core.page  import  Page

# THEN ADD A LINK TO DISPLAY THE OBJECT
class History(Page):
       def results(self):
           return getHistory(self.context,last=200)

       def pp(self,item):
           return pp(item)
       template = tal_template('history.pt')


class HistoricIndex(Page):
       def item(self):
           offset=self.request.form['offset']
           offset = int(offset)
           item= getHistory(self.context)[offset]['obj']
           return item

       def render(self ):  
           return self.item().source


class HistoricView (HistoricIndex):
       def render(self ):  
           return self.item()(self)


class Restore(HistoricIndex):
       def render(self ):  
           self.context.title=self.item().title
           self.context.source=self.item().source
           return self.redirect(self.url(self.context)+'/aceEdit')


