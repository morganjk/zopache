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

class Form(BaseForm,Scripts):
    responseFactory = Response
    make_response = make_layout_response
    template = tal_template('form.pt')

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

