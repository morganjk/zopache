from zope.location.location import LocationIterator
from zope.interface import Interface




# JUST  PARENTAL (NO ZCLASS) ACQUISITION OF OBJECTS IN CONTAINERS
class Acquire (object):
  def __init__(self,context):
      self.context=context
      
  def __getitem__(self,name,default=object) :
     context=self.context
     _marker = default  

     #FIRST SEE IF THIS ITEM HAS THE VALUE
     if hasattr(context, '__getitem__'):
            result =context.get(name, _marker)
            if result!=_marker:
               return result

     #IF NOT CHECK THE PARENT CLASSES
     for item in LocationIterator(self.context):
       if hasattr(item, '__getitem__'):
         result =item.get(name, _marker)
         if result!=_marker:
            return result







