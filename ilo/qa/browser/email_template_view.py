from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.email_template import IEmailTemplate

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IEmailTemplate)
    grok.require('zope2.View')
    grok.template('email_template_view')
    grok.name('view')

