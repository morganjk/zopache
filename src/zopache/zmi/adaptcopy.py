#SUBJECT TO THE CV LICENSE AGREEMENT

#SO WHAT IS GOING ON HERE?
import crom
from zope.copy.interfaces import ICopyHook, ResumeCopy
from zope.interface import Interface
from zope.interface import implementer, Invalid
from cromdemo.interfaces import ITreeLeaf
from cromdemo.models  import TreeLeaf

@crom.adapter
@crom.sources(Interface)
@crom.target(ICopyHook)
def location_copyfactory(obj):
         def factory(location, register):
             raise ResumeCopy
         return factory
