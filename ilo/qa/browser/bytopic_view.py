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
        brains = catalog.searchResults(path={'query': path, 'depth' : 2}, portal_type='ilo.qa.topic',review_state='enabled',sort_on='Date',sort_order='reverse')
        for brain in brains:
            results.append({'value':brain.getId,
                            'name':brain.Title})
        return results


    def searchedValue(self, name=None):
        result = ''
        if self.request.form:
            form = self.request.form
            if not form.has_key('data'):
                form['data']=0
            if not form.has_key('data1'):
                form['data1']=0
            result = form[name]
        return result

    def contents(self):
        context = self.context
        request = self.request
        form = request.form
        catalog = self.catalog
        topic=''
        has_answer_results = []
        no_answer_results = []
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(path={'query': path, 'depth' : 2}, portal_type='ilo.qa.question',
                                                    # review_state='shared_intranet,
                                                    sort_on='Date',
                                                    sort_order='reverse')
        if form:
            topic = form['topic1']
        for brain in brains:
            obj = brain.getObject()
            if topic in self.pledge_id(obj.topic):
                answers = catalog.searchResults(path={'query': brain.getPath(), 'depth' : 1}, 
                                                portal_type='ilo.qa.answer')
                
                if answers and answers[0].review_state != 'draft':
                    has_answer_results.append(brain)
                
                answer_draft = ''
                if not answers or answers[0].review_state == 'draft':
                    if answers:
                        answer_draft = answers[0]
                    no_answer_results.append({'brain':brain, 'answer_draft': answer_draft})
        return (has_answer_results, topic, no_answer_results)

    def pledge_id(self, uids = None):
        catalog = self.catalog
        context = self.context
        results = []
        path = '/'.join(context.getPhysicalPath())
        for uid in uids or []:
            brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, 
                                                        portal_type='ilo.qa.topic',
                                                        UID = uid)
            for brain in brains:
                results.append(brain.getId)
        return results

    def pledge_title(self, uid = None):
        catalog = self.catalog
        context = self.context
        title = []
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, 
                                                    portal_type='ilo.qa.topic', 
                                                    id = uid)
        for brain in brains:
            title.append(brain.Title)
        return title









