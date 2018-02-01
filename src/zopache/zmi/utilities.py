from dolmen.container import IBTreeContainer
import arrow
from zopache.core import getRoot

def size(item):
    result=1
    if IBTreeContainer.providedBy(item):
        for child  in item.values():
            result+=size(child)
    return result

"GET THE ROOT FOLDER"     
def pasteFolder(self):
        return getRoot(self).pasteFolder
