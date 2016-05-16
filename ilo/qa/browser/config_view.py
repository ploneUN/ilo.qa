from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.config import Iconfig
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(Iconfig)
    grok.require('zope2.View')
    grok.template('config_view')
    grok.name('view')

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def contents(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, 
                                                    portal_type='ilo.qa.topic',
                                                    sort_order='title')
        return brains

