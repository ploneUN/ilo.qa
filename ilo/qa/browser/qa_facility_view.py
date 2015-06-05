from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.qa_facility import IQAFacility

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IQAFacility)
    grok.require('zope2.View')
    grok.template('qa_facility_view')
    grok.name('view')

