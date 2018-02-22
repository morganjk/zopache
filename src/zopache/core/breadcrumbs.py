#Subject to ZPL and CV Licenses
# -*- coding: utf-8 -*-

from cromlech.browser import IPublicationRoot
from cromlech.location import lineage_chain
from cromlech.location import resolve_url
from cromlech.location import get_absolute_url
from dolmen.container import IBTreeContainer

try:
  from zopache.ttw.acquisition import Acquire
except ImportError:
  Acquire=lambda x : x      

try:
        from urllib import quote  # Python 2.X
except ImportError:
        from urllib.parse import quote  # Python 3+

_safe = '@+'  # Characters that we don't want to have quoted



def nameAndTitle(item,showTitles):
        """Choose a display name for the current context.
        This method has been splitted out for convenient overriding.
        """
        name = getattr(item, '__name__', None)
        title= getattr(item, 'title', None)
    
        if name is None and not IPublicationRoot.providedBy(item):
            raise KeyError('Object name (%r) could not be resolved.' % item)
    
        if (title != None) and showTitles:
            return name, title
        return name, name


class Breadcrumbs(object):
    
    def breadcrumbsIndex(self,item):
        return self.breadcrumbsView(item,viewName='',showTitles=True)
    
    def breadcrumbsManage(self):
        return self.breadcrumbsView(self.context,viewName='manage',showTitles=False)
    
    def breadcrumbs(self):
            return self.breadcrumbsIndex(self.context)
            
    def breadcrumbsView(self,item, viewName='',showTitles=True):
        return  self.breadcrumbsCore(item,
                                     viewName=viewName,
                                     showTitles=showTitles)
    
    def breadcrumbsCore(self,item,
                        viewName='',
                        showTitles=True,
                        resolver=nameAndTitle):
        #IF YOU WANT A SPECFIC VIEWNAME, THEN PREPEND A SLASH
        slashViewName =''             
        if viewName != '':
           slashViewName ='/' + viewName
    
        parents = lineage_chain(item)
        result=[]
        if parents:
            parents.reverse()
            root = parents.pop(0)
            base_url = ''
            name, title = resolver(root,showTitles)
            if viewName == '':
                result.append( self.href('/',title))
            else:    
                result.append( self.href(slashViewName,title))
                                
            for ancestor in parents:
                name, title = resolver(ancestor,showTitles)
                base_url += '/' + quote(name.encode('utf-8'), _safe)
                result.append( self.href(base_url + slashViewName,title))
        return ' / '+' / '.join(result)

    
    def isBTreeContainer(self):
         return  IBTreeContainer.providedBy(self.context)    

    def objectHref(self,obj,name):
        return self.href(self.url(obj),name)
    
    def href(self,url,name):
           result ='<a href=\"'
           result += url
           result+='\">'
           if name != None:
              result += name
           result +='</a>'
           return result

    def acquire(self,name):
            return Acquire(self)[name]

    def acquireTitle(self):
        parents = lineage_chain(self.context)
        parents.reverse()
        for item in parents:
            if (hasattr(item,'title') and
               item.title!=''):
               return item.title
        return ''


    def url(self, *args):
        if len(args)==0:
           return get_absolute_url(self.context, self.request)
        else:
            return  get_absolute_url((args)[0], self.request)
           
    #And here is a much simpler implementation of URL.
    #Only good for this zodb application. 
    def simpleUrl(self,item):
        import pdb; pdb.set_trace()
        if IPublicationRoot.providedBy(item):
           return self.request.application_url
        container = item.__parent__
        result = self.url(container)+ '/' + item.__name__
        return result

   
