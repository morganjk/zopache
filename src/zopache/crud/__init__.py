#!/usr/bin/python
# -*- coding: utf-8 -*-

from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("dolmen.forms.crud")


from zopache.crud.actions import (
    AddAction, UpdateAction, DeleteAction, CancelAction)
from zopache.crud.components import DisplayForm, AddForm, EditForm, DeleteForm

from zopache.crud.interfaces import (
    ILeaf, IContainer, IRootContainer, IAddable, IEditable, IDeletable, IDisplayable, IRenameable)
