#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("dolmen.forms.crud")


from zopache.crud.actions import (
    AddAction,
    UpdateAction,
    DeleteAction,
    CancelAction,
    AddAndAceEditAction,
    AddAndCkEditAction,
    AddAndViewAction,
    AddAndManageAction)

from zopache.crud.components import DisplayForm, AddForm, EditForm, DeleteForm

from zopache.crud.interfaces import (
    ILeaf, IContainer, IRootContainer, IAddContainer, IEditable, IDeletable, IDisplayable, IRenameable)

from os import path
TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')
def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))    
