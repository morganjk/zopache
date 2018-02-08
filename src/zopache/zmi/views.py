from zope import schema
from zope import interface
from cromlech.container.interfaces import IBTreeContainer
from zopache.ttw.acquisition import Acquire
from zopache.zmi.contents import Contents
from zopache.core import Page
from zopache.core.page  import  Page
from . import tal_template
from crom import target, order
from dolmen.view import name, context, view_component
from cromlech.browser.directives import title
from dolmen.container import IBTreeContainer
from cromdemo.interfaces import ITab
from .contents import Contents

@view_component
@name('manage')
@title("Manage")
@target(ITab)
@context(IBTreeContainer)
class Manage(Page,Contents):
    label='Manage Folder'
    template = tal_template('zmi.pt')
    def breadcrumbs(self):     
        return self.breadcrumbsManage(self)
    
#USED TO FIRE UP A DEBUGGER TO MAKE MANUAL CHANGES    
class Fix(Manage):
       def update(self):
          item=self.context
          import pdb; pdb.set_trace()
          from privacv.skill import doit
          doit(item)
          resource.style.need()






       

       



