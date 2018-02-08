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


def uniqueName(target, new_name,ofType="Copy"):
        count=0
        copyName=new_name+ofType
        while target.has_key(new_name):
               count +=1
               new_name=copyName+str(count)
        return new_name
    
