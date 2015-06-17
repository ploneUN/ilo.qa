from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.qa_facility import IQAFacility
from Products.CMFCore.utils import getToolByName


grok.templatedir('templates')

class bytopic_view(dexterity.DisplayForm):
    grok.context(IQAFacility)
    grok.require('zope2.View')
    grok.template('bytopic_view')

    @property
    def catalog(self):
    	return getToolByName(self.context, 'portal_catalog')

    def topic(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        results = [{'value':'all', 'name':'All'}]
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.topic',review_state='published',sort_on='Date',sort_order='reverse')
        for brain in brains:
            results.append({'value':brain.UID,
                            'name':brain.Title})
        return results


    def searchedValue(self, name=None):
        result = ''
        if self.request.form:
            form = self.request.form
            result = form[name]
        return result


    def contents(self):
        context = self.context
        request = self.request
        form = request.form
        catalog = self.catalog
        topic=''
        results = []
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.question',review_state='published',sort_on='Date',sort_order='reverse')
        if form:
            topic = form['topic']
        i = 0
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if topic in obj.topic:
                i = i + 1
                results.append({'title': brain.Title,
                                'path':brain.getPath()})
                if i == 10:
                    break;
            if topic == 'all':
                i = i + 1
                results.append({'title': brain.Title,
                                'path':brain.getPath()})
                if i == 10:
                    break;
        return results










