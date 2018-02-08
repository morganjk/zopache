from dolmen.forms.base import action, name, context, form_component
from zopache.crud.forms import AddForm, EditForm
from zope.cachedescriptors.property import CachedProperty
from dolmen.forms.base import action, name, context, form_component
from dolmen.forms.base import Actions
from zopache.crud import actions as formactions, i18n as _

class AceEditForm(EditForm):
    @CachedProperty
    def actions(self):
        return Actions(
              formactions.SaveAndAceEdit(_("Save","Save")),
              formactions.SaveAndView(_("Save  and View","Save -> View")),
              formactions.CancelAction(_("Cancel","Cancel")))
	      
class AceAddForm (AddForm):
    @CachedProperty
    def actions(self):
        return Actions(
              formactions.SaveAndAceEdit(_("Save","Save")),
              formactions.SaveAndView(_("Save  and View","Save -> View")),
              formactions.CancelAction(_("Cancel","Cancel")))
