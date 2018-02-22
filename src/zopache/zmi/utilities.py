from dolmen.container import IBTreeContainer
import arrow

#THERE IS A COPY OF THIS IN zopache.core  as well       
from cromlech.browser.interfaces import IPublicationRoot

def getRoot(object):
        max = 9999
        context=object
        while context is not None:
            if IPublicationRoot.providedBy(context):
                return context
            context = context.__parent__
            max -= 1
            if max < 1:
                raise TypeError("Maximum location depth exceeded, "                                "probably due to a a location cycle.")
        raise TypeError("Parents needed to  determine location root")

def size(item):
    result=1
    if IBTreeContainer.providedBy(item):
        for child  in item.values():
            result+=size(child)
    return result

"GET THE ROOT FOLDER"     
def pasteFolder(self):
        return getRoot(self).pasteFolder


    
