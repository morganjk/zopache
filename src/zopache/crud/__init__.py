#!/usr/bin/python
# -*- coding: utf-8 -*-
from dolmen.template import TALTemplate

from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("zopache.crud")

from os import path
TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')
def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))    



