from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.topic import ITopic

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(ITopic)
    grok.require('zope2.View')
    grok.template('topic_view')
    grok.name('view')

