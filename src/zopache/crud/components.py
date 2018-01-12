# -*- coding: utf-8 -*-

from dolmen.forms.base import Form, DISPLAY
from zopache.crud import actions as formactions, i18n as _
from zopache.crud.utils import getFactoryFields, getAllFields
from cromlech.i18n import translate

from dolmen.forms.base import Actions
from zope.cachedescriptors.property import CachedProperty
from zope.i18nmessageid import Message
from .interfaces import IName

from dolmen.forms.base import Fields
from cromlech.webob import Response

#So we add a response factory
#Becasue Form does not have it. If you are building an asyncio
#server, then you have a very different response class.
class Form (Form):
    def responseFactory(self, status=None, headers=None):
        if (status !=None or headers!=None):
           response= Response(status=status,headers=headers)
        else:
            response = Response() 
        return response
    
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


class DeleteForm(Form):
    """A confirmation for to delete an object.
    """
    description = _(u"Are you really sure ?")
    actions = Actions(formactions.DeleteAction(_("Delete","Delete")),
                      formactions.CancelAction(_("Cancel","Cancel")))

    @property
    def label(self):
        label = _(u"delete_action", default=u"Delete: $name",
                  mapping={"name": title_or_name(self.context)})
        return translate(label)

class RenameForm(Form):
     pass
