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
        
    def officer_details(self, officer=None):
        membership = getToolByName(self.context, 'portal_membership')
        image = membership.getPersonalPortrait().absolute_url()
        try:
            name = membership.getMemberById(officer)
            email = name.getProperty('email')
            fullname = name.getProperty('fullname')
            image = membership.getPersonalPortrait(officer).absolute_url()
        except AttributeError:
            email = ''
            fullname = ''
        return {'image': image,
                'email': email,
                'fullname': fullname}
    
    def officers_contents(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        results = {}
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 2}, 
                                                    portal_type='ilo.qa.topic',
                                                    review_state='enabled')
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if obj.officer:
                officer = obj.officer
                if officer not in results:
                    results[officer] = {}
                    results[officer]['name'] = officer
                    results[officer]['officer_title'] = obj.officer_title
                    results[officer]['uid'] = brain.UID
                    results[officer]['data'] = [{'title':brain.Title,
                                                 'id':brain.getId,
                                                 'uid':brain.UID}]
                else:
                    results[officer]['data'].append({'title':brain.Title,
                                                     'id':brain.getId,
                                                     'uid':brain.UID})
        officer_titles = ['Director', 'Senior Evaluation Officer', 'Communications and Knowledge Management Officer']
        data = []
        if results:
            data = [results[val] for val in results]
            data.sort(key=lambda x:officer_titles.index(x.get('officer_title')) if x.get('officer_title') in officer_titles else 99)
        return data
                    
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