# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from os import path

from cromlech.webob.response import Response
from dolmen.view import View, make_layout_response
from dolmen.forms.base import Form as BaseForm
from cromlech.location import get_absolute_url
from cromlech.browser.interfaces import IURL, IPublicationRoot

class Page(View):
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
