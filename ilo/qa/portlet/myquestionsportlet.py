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
    
    button_label = schema.TextLine(
            title = u"Button Label",
            required=False,
        )
    

class Assignment(base.Assignment):
    implements(IContentNavigation)
    
    
    def __init__(self, button_label=None):
        self.button_label = button_label
       
       
    @property
    def title(self):
        return "My Questions Button Portlet"
    
class Renderer(base.Renderer):
    render = ViewPageTemplateFile('templates/myquestionsportlet.pt')
    def __init__(self, context, request, view, manager, data):
        self.context = context
        self.request = request
        self.view = view
        self.manager = manager
        self.data = data
        
    def contents(self):
        return self.data
    
    def myquestions_url(self):
        return self.context.absolute_url()+'/my_questions_view'
    

class AddForm(base.AddForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Add My Questions Button Portlet"
    description = ''
    
    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(IContentNavigation)
    # form_fields['item_title'].custom_widget = WYSIWYGWidget
    label = u"Add My Questions Button Portlet"
    description = ''
    
    
