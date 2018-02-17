from dolmen.container import IBTreeContainer, BTreeContainer
from zope.interface import implementer
from zopache.crud import actions as formactions, i18n as _
from cromlech.security import getSecurityGuards, permissions
from zope.cachedescriptors.property import CachedProperty
from zope.interface import implementer
from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component
from zopache.core.forms import Form
from cromlech.browser.directives import title
from zopache.ttw.html import HTML
from .interfaces import IHTMLContainer
from zopache.ttw.html import TrustedHTML
from zopache.crud.forms import AddForm
from zope.interface import Interface

@implementer(IHTMLContainer)
class HTMLContainer(TrustedHTML,BTreeContainer):
    icon="ttwicons/Container.svg"
    def __init__(self):
        BTreeContainer.__init__(self)



from zopache.crud.interfaces import IWeb    
@form_component
@name (u'addContainer')
@context(IBTreeContainer)
@title("Add TTWContainer.")
@permissions('Manage')
@implementer(IWeb)
class AddContainer(AddForm):
    subTitle = 'Add a Container'
    interface = Interface
    ignoreContent = True
    factory=HTMLContainer

    @CachedProperty
    def actions(self):
        return Actions(
              formactions.AddAndManage(_("Add and Manage","Add and Manage"), self.factory),
              formactions.AddAndCkEdit(_("Add and ckEdit","Add and CkEdit"), self.factory),
              formactions.AddAndAceEdit(_("Add and AceEdit","Add and AceEdit"), self.factory),
              formactions.Cancel(_("Cancel","Cancel")))        
