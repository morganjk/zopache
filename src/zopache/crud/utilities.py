def uniqueName(target, new_name,ofType="Copy"):
        count=0
        copyName=new_name+ofType
        while target.has_key(new_name):
               count +=1
               new_name=copyName+str(count)
        return new_name

def title_or_name(obj):
    title = getattr(obj, 'title', None)
    if title is not None:
        return title
    return getattr(obj, '__name__', u'')
