#Subject to ZPL and CV Licenses
# -*- coding: utf-8 -*-

from cromlech.browser import IPublicationRoot
from cromlech.location import lineage_chain
from cromlech.location import resolve_url
from cromlech.location import get_absolute_url
from dolmen.container import IBTreeContainer
from zopache.zmi.interfaces import IURLSegment

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
    

    def slashViewName(self,item, viewName):      
            slashViewName =''
            if viewName == '':
                if IPublicationRoot.providedBy(item):
                   return '/'
                else:
                   return ''
            elif viewName=='manage':
               return '/' + IURLSegment(item).getSegment()
            else:    
                return '/' + viewName
                
    def breadcrumbsCore(self,item,
                        viewName='',
                        showTitles=True,
                        resolver=nameAndTitle):

        parents = lineage_chain(item)
        result=[]
        base_url = ''
        if parents:
            parents.reverse()
            for ancestor in parents:
                name, title = resolver(ancestor,showTitles)
                slashViewName = self.slashViewName(ancestor,viewName)
                base_url += '/' + quote(name.encode('utf-8'), _safe)
                result.append( self.href(base_url + slashViewName,title))
        return ' / '+' / '.join(result)

    
    def isBTreeContainer(self,*args):
        if (len (args)==0):
           return  IBTreeContainer.providedBy(self.context)    
        return  IBTreeContainer.providedBy(args[0])    

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
        if IPublicationRoot.providedBy(item):
           return self.request.application_url
        container = item.__parent__
        result = self.url(container)+ '/' + item.__name__
        return result

   
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
