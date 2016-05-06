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
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, portal_type='ilo.qa.topic',review_state='internally_published',sort_on='Date',sort_order='reverse')
        for brain in brains:
            results.append({'value':brain.getId,
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
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, portal_type='ilo.qa.question',review_state='internally_published',sort_on='Date',sort_order='reverse')
        if form:
            topic = form['topic1']
        i = 0

        for brain in brains:
            obj = brain._unrestrictedGetObject()
            #import pdb; pdb.set_trace()
            if topic in self.pledge_id(obj.topic):
                i = i + 1
                results.append({'title': brain.Title,
                                'path':brain.getPath()})
                if i == 11:
                    break;
            if topic == 'all':
                i = i + 1
                results.append({'title': brain.Title,
                                'path':brain.getPath()})
                if i == 11:
                    break;
        return (results, self.pledge_title(topic))

    def pledge_id(self, uids = None):
        catalog = self.catalog
        context = self.context
        results = []
        path = '/'.join(context.getPhysicalPath())
        for uid in uids:
            brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, portal_type='ilo.qa.topic',UID = uid)
            for brain in brains:
                results.append(brain.getId)
        return results

    def pledge_title(self, uid = None):
        catalog = self.catalog
        context = self.context
        title = []
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, portal_type='ilo.qa.topic', id = uid)
        for brain in brains:
            title.append(brain.Title)
        return title









