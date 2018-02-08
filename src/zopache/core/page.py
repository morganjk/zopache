# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from os import path
from zopache.crud.interfaces import IWeb
from cromlech.webob.response import Response
from dolmen.view import View, make_layout_response
from dolmen.forms.base import Form as BaseForm
from cromlech.location import get_absolute_url
from cromlech.browser.interfaces import IURL, IPublicationRoot
from .scripts import Scripts
from dolmen.container import IBTreeContainer
from .breadcrumbs import Breadcrumbs

class Page(View,Scripts,Breadcrumbs):
    count=0
    responseFactory = Response
    make_response = make_layout_response

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


    # Don't show add HTML CSS Javascript Image
    #def contentItems(self):
            
#if IWeb.implementedBy(aClass):
 #                  continue       
