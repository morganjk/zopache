# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from cromlech.webob.response import Response

from dolmen.template import TALTemplate
from dolmen.view import View, make_layout_response
from dolmen.forms.base import Form as BaseForm
from cromlech.location import get_absolute_url

from . import tal_template

from .scripts import Scripts

from dolmen.container import IBTreeContainer
from .breadcrumbs import Breadcrumbs
class Form(BaseForm,Scripts,Breadcrumbs):
    title=""
    subTitle=u""
    responseFactory = Response
    make_response = make_layout_response
    template = tal_template('form.pt')
    def widgetDictionary(self):
        return {c.htmlId():c for c in self.bootstrap_widgets()}

    def fieldDictionary(self):
        return {c.__name__:c for c in self.fields}    


    def bootstrap_widgets(self):
        """Adds the needed css classes for bootstrap styles.
        """
        for widget in self.fieldWidgets:
            widget.defaultHtmlClass.append('form-control')
            yield widget

    def isBTreeContainer(self):
         return  IBTreeContainer.providedBy(self.context)

    #USED BY HTML TO COMPILE THE TEMPLATE
    def postProcess(self):
         pass

    def breadcrumbs(self):     
        return self.breadcrumbsManage()

    def debug(self):
         import pdb; pdb.set_trace()
         pass

    def url(self):
        return get_absolute_url(self.context, self.request)     
