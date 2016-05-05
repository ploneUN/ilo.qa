from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.qa_facility import IQAFacility
from Products.CMFCore.utils import getToolByName
from plone import api

grok.templatedir('templates')

class my_questions_view(dexterity.DisplayForm):
    grok.context(IQAFacility)
    grok.require('zope2.View')
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    @property
    def membership(self):
        return getToolByName(self.context, 'portal_membership')
    
    def topic_val(self, uid):
        if uid:
            brains = self.context.portal_catalog({'uid':uid, 'portal_type':'ilo.qa.topic'})
            for brain in brains:
                return brain.Title
        return ''
    
    def get_answer(self, path):
        brains = self.catalog.searchResults(path={'query':path, 'depth':1}, portal_type='ilo.qa.answer', sort_on='modified', sort_order='descending')
        if brains:
            return brains[0].Title
            
        
        
    
    def questions(self):
        auth_user = self.context.portal_membership.getAuthenticatedMember().getUserName()
        results = []
        brains = self.context.portal_catalog({'path':{'query':'/'.join(self.context.getPhysicalPath()),
                                                      'depth':1},
                                              'portal_type':'ilo.qa.question'})
        for brain in brains:
            
            if brain.Creator == auth_user:
                raw = {}
                raw['title'] = brain.Title
                raw['topic'] = ''
                
                topics = brain.getObject().topic
                for tp in topics:
                    raw['topic'] += self.topic_val(tp)
                raw['answer'] = self.get_answer(brain.getPath())
                raw['state'] = brain.review_state.title().replace('_', ' ')
                raw['url'] = brain.getObject().absolute_url()
                results.append(raw)
        return results
                
        