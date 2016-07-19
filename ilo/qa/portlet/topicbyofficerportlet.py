from five import grok
from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.component import getMultiAdapter
from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
from Products.CMFCore.utils import getToolByName
from operator import itemgetter
from zope.component.hooks import getSite



grok.templatedir('templates')

class IContentNavigation(IPortletDataProvider):
    
    portlet_title = schema.TextLine(
            title = u"Officer Portlet Title",
            required=False,
        )


class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    
    def __init__(self, portlet_title=None):
        self.portlet_title = portlet_title
       
       
    @property
    def title(self):
        return "Topic By Officer Portlet"
    

class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/topicbyofficerportlet.pt')
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.data = data
        
        
    def contents(self):
        return self.data

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def officers_contents(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        results = []
        gen_officer = 'General Officer'
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, 
                                                    portal_type='ilo.qa.topic',
                                                    review_state='enabled')
        # for brain in brains:
        #     obj = brain._unrestrictedGetObject()
        #     #if not any(d['name'].lower() == obj.officer.lower() for d in results) and obj.officer.lower() != gen_officer.lower():
        #     brain_dict =  {'name':obj.officer.lower(),
        #                     'officer_title':obj.officer_title,
        #                     'officer_email': obj.officer_email,
        #                     'uid':brain.UID,
        #                     'data': self.topics(obj.officer.lower(),brains)}
           
        #     if not any(d['name'].lower() == obj.officer.lower() for d in results) and obj.officer.lower() != gen_officer.lower():
        #         if obj.officer_title != 'Director':
        #             results.append(brain_dict)
        #         else:
        #             results.insert(0, brain_dict)

        #     if obj.officer.lower() == gen_officer.lower():
        #         general_officer.append(brain_dict)

        # #results.sort(key=lambda x: ['Director', 'Sales','Officer'].index(x['officer_title']))
        # return {'data': results, 
        #         #'data': sorted(results, key=itemgetter('name')), 
        #         'general_officer': general_officer}
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            brain_dict =  {'name':obj.officer.lower(),
                            'officer_title':obj.officer_title,
                            'officer_email': obj.officer_email,
                            'uid':brain.UID,
                            'data': self.topics(obj.officer.lower(),brains)}
           
            if not any(d['name'].lower() == obj.officer.lower() for d in results):
                results.append(brain_dict)
        officer_titles = ['Director', 'Senior Evaluation Officer', 'Communications and Knowledge Management Officer']
        results.sort()
        results.sort(key=lambda x: officer_titles.index(x.get('officer_title')) if x.get('officer_title') in officer_titles else 99)
        return results

    def topics(self, officer, brains):
        topics = []
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if obj.officer.lower() == officer :
                topics.append({'title': brain.Title,
                                'id': brain.getId,
                                'uid':brain.UID})
        return topics
        
    def officer_photo(self, officer_email=None):
        membership = getToolByName(self.context, 'portal_membership')
        userImg = membership.getPersonalPortrait().absolute_url()
        for member in membership.listMembers():
            if officer_email == member.getProperty('email'):
                user_id = member.getUserName()
                userImg = membership.getPersonalPortrait(user_id).absolute_url()
    
        return userImg


class AddForm(base.AddForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Add Topic By Officer Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Edit Topic By Officer Portlet"
    description = ''