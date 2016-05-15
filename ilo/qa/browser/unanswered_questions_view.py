from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.qa_facility import IQAFacility
from Products.CMFCore.utils import getToolByName

grok.templatedir('templates')

class unanswered_questions_view(dexterity.DisplayForm):
    grok.context(IQAFacility)
    grok.require('zope2.View')
    

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def contents(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        results = []
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.question',review_state='shared_intranet',sort_on='Date',sort_order='reverse')
        for brain in brains:
            brains2 = catalog.unrestrictedSearchResults(path={'query':brain.getPath(), 'depth':1}, portal_type='ilo.qa.answer', review_state='shared_intranet')
            if len(brains2) == 0:
                results.append({'title':brain.Title, 'path':brain.getPath()})
        return results
