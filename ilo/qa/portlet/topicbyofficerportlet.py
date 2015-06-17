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
        return "Add Selfie"
    

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

    def topic(self):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        results = [{'value':'all', 'name':'All'}]
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.topic',review_state='published',sort_on='Date',sort_order='reverse')
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if not any(d['name'] == obj.officer for d in results):
                results.append({'value':obj.officer,
                                'name':obj.officer})
        return results

    def searchedValue(self, name=None):
        result = ''
        if self.request.form:
            form = self.request.form
            result = form[name]
        return result


    def contents1(self):
        context = self.context
        request = self.request
        form = request.form
        catalog = self.catalog
        topic=''
        results = []
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.topic',review_state='published',sort_on='Date',sort_order='reverse')
        if form:
            topic = form['topic']
        i = 0
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            if topic in obj.officer:
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
