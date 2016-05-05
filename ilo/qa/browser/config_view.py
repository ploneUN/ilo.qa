from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.config import Iconfig

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(Iconfig)
    grok.require('zope2.View')
    grok.template('config_view')
    grok.name('view')

