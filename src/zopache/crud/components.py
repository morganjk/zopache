# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.

from dolmen.forms.base import DISPLAY
from zopache.crud import actions as formactions, i18n as _
from zopache.crud.utils import getFactoryFields, getAllFields
from cromlech.i18n import translate
from cromlech.browser.directives import title
from cromlech.security import getSecurityGuards, permissions


from zope.cachedescriptors.property import CachedProperty
from zope.i18nmessageid import Message
from .interfaces import IName, IContainer
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component

from cromlech.webob import Response
from .interfaces import IEditable, IDeletable, IDisplayable
from zopache.core.forms import Form

    
def title_or_name(obj):
    title = getattr(obj, 'title', None)
    if title is not None:
        return title
    return getattr(obj, '__name__', u'')


class AddForm(Form):
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    @property
    def label(self):
        name = getattr(self.factory, 'name', None)
        if name is not None:
            if isinstance(name, Message):
                name = translate(name)
            return translate(
                _(u"add_action", default="Add: $name",
                  mapping={'name': name}))
        return 'Add'

    @CachedProperty
    def fields(self):
        if hasattr(self,'interface'):
            return  Fields(IName,self.interface).omit("__parent__")
        return Fields()


        return self.fields('__parent__', '__name__')

    @CachedProperty
    def actions(self):
        return Actions(
              formactions.AddAction(_("Add","Add"), self.factory),
              formactions.CancelAction(_("Cancel","Cancel")))


@implementer(IContainer)
class CrudContainer(BTreeContainer):
    pass
    
@form_component
@name (u'addContainer')
@context(IBTreeContainer)
@title("Add a Container")
@permissions('Manage')
class AddContainer(AddForm):
        interface = IContainer
        ignoreContent = True
        factory=CrudContainer

@form_component
@name (u'edit')
@context(IEditable)
@title("Edit")
@permissions('Manage')    
@title("Edit")
@permissions('Manage')
class EditForm(Form):
    """
    """
    ignoreContent = False
    ignoreRequest = False
    actions = Actions(formactions.UpdateAction(_("Update","Update")),
                      formactions.CancelAction(_("Cancel","Cancel")))

    @property
    def label(self):
        label = _(u"edit_action", default=u"Edit: $name",
                  mapping={"name": title_or_name(self.context)})
        return translate(label)

    @CachedProperty
    def fields(self):
        edited = self.getContentData().getContent()
        return getAllFields(edited, '__parent__', '__name__')

@form_component
@name (u'display')
@context(IDisplayable)
@title("Display")
@title("Display")
@permissions('Manage')    
class DisplayForm(Form):
    """
    """
    mode = DISPLAY
    ignoreRequest = True
    ignoreContent = False

    @property
    def label(self):
        return title_or_name(self.context)

    @CachedProperty
    def fields(self):
        displayed = self.getContentData().getContent()
        return getAllFields(displayed, '__parent__', '__name__', 'title')

@form_component
@name (u'delete')
@context(IDeletable)
@title("Delete")
@permissions('Manage')    
@title("Delete")
class DeleteForm(Form):
    """A confirmation for to delete an object.
    """
    description = _(u"Are you really sure ? This will also delete all of its children.")
    actions = Actions(formactions.DeleteAction(_("Delete","Delete")),
                      formactions.CancelAction(_("Cancel","Cancel")))

    @property
    def label(self):
        label = u"Delete This Object?" 
        return translate(label)

    
class RenameForm(Form):
     pass
