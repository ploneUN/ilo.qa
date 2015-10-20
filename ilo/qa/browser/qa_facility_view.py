from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.qa_facility import IQAFacility
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IQAFacility)
    grok.require('zope2.View')
    grok.template('qa_facility_view')
    grok.name('view')

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def contents(self):
    	context = self.context
    	catalog = self.catalog
    	path = '/'.join(context.getPhysicalPath())
    	brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.question',review_state='internally_published',sort_on='Date',sort_order='reverse')[:10]
    	return brains

    def topic(self, uids = None):
        catalog = self.catalog
        context = self.context
        results = []
        path = '/'.join(context.getPhysicalPath())
        for uid in uids:
            brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.topic',UID = uid)
            for brain in brains:
                results.append(brain.Title)
        return ', '.join(results)