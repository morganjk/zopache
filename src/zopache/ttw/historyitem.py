import crom
from zope.location import Location
from cromlech.browser import ITraverser, IRequest
from zopache.ttw.interfaces import IHistoryItem
from zope.interface import implementer
from zope.interface import Interface
from dm.historical import getHistory

@implementer(IHistoryItem)
class HistoryItem(Location):

    def __init__(self, item, offset):
        self.offset = offset
        self.item = item


@crom.adapter
@crom.sources(Interface, IRequest)
@crom.target(ITraverser)
@crom.name('history')
class HistoryTraverser(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, ns, name):
        idx = int(name)
        history = getHistory(self.context)
        assert idx < len(history)
        history_item = HistoryItem(history[idx], idx)
        history_item.__parent__ = self.context
        history_item.__name__ = '++%s++%s' % (ns, name)
        return history_item
