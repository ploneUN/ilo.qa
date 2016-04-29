from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from zope.interface import alsoProvides

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder
#from plone.multilingualbehavior.directives import languageindependent
from collective import dexteritytextindexer

from ilo.qa import MessageFactory as _

from Products.CMFCore.utils import getToolByName
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from plone.i18n.normalizer import idnormalizer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


# Interface class; used to define content-type schema.

#pledge detail vocabulary for dropdown
class topics(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context ):
        catalog = getToolByName(context, 'portal_catalog')
        #brains = catalog.unrestrictedSearchResults(object_provides = IPledgeDetail.__identifier__,sort_on='sortable_title', sort_order='ascending', review_state='published')
        if context.portal_type == 'ilo.qa.qafacility':
            path = '/'.join(context.getPhysicalPath())
        else:
            path = '/'.join(context.aq_parent.getPhysicalPath())
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, 
                                                    portal_type='ilo.qa.topic',
                                                    review_state='internally_published',
                                                    sort_on='sortable_title')
        results = []
        for brain in brains:
            obj = brain._unrestrictedGetObject()
            results.append(SimpleTerm(value=brain.UID, token=brain.UID, title=brain.Title))
        return SimpleVocabulary(results)

class IQuestion(form.Schema, IImageScaleTraversable):
    """
    Question
    """
    # topic = schema.TextLine(
    #        title=_(u"Topic"),
    #        required=True,
    #     )
    # topic = schema.Choice(title = u"Topic",source=topics(), required=True)

    title = schema.TextLine(
           title=_(u"Question Title"),
           required=True,
        )

    dexteritytextindexer.searchable('question_details')
    form.widget(question_details=WysiwygFieldWidget)
    question_details = schema.Text(title=u"Question Details")


    form.widget(topic=CheckBoxFieldWidget)
    topic = schema.List(
        title=u'Topic',
        required=False,
        value_type=schema.Choice(source=topics())
    )
    
    dexteritytextindexer.searchable('question_creator')
    form.mode(question_creator='hidden')
    question_creator = schema.TextLine(
           title=_(u"Question Creator"),
           required=False,
        )

    dexteritytextindexer.searchable('topic_officer')
    form.mode(topic_officer='hidden')
    topic_officer = schema.TextLine(
           title=_(u"Topic Creator"),
           required=False,
        )
    
    dexteritytextindexer.searchable('topics_str')
    form.mode(topics_str='hidden')
    topics_str = schema.TextLine(
        title = _(u"Topics"),
        required = False,
    )
    pass

alsoProvides(IQuestion, IFormFieldProvider)

def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False

@grok.subscribe(IQuestion, IObjectAddedEvent)
def _createObject(context, event):
    catalog = getToolByName(context, 'portal_catalog')
    membership = getToolByName(context, 'portal_membership')
    topic_officer = []
    topics = []
    parent = context.aq_parent
    id = context.getId()

    if context.topic:
        brains = catalog.unrestrictedSearchResults(portal_type='ilo.qa.topic', UID=context.topic)
        for brain in brains:
            #if membership.getMemberById(brain.Creator).getProperty('email'):
            #    topic_officer.append(membership.getMemberById(brain.Creator).getProperty('email'))
            topic_officer.append(brain._unrestrictedGetObject().officer_email)
            topics.append(brain.Title)
    if topic_officer:
        context.topic_officer = ','.join(topic_officer)
    
    if membership.getMemberById(context.Creator()).getProperty('email'):
        context.question_creator = membership.getMemberById(context.Creator()).getProperty('email')
    if topics:
        context.topics_str = '\n'.join(topics)
    
    object_ids = context.aq_parent.objectIds()
    title = idnormalizer.normalize(context.Title())
    
    if title in object_ids:
        id_num = []
        for ids in object_ids:
            if ids.startswith(title):
                val = ids.replace(title, '').split('-')
                if is_number(val[-1]):
                    id_num.append(int(val[-1]))
        if id_num:
            parent.manage_renameObject(id, title+'-'+str(max(id_num)+1))
        else:
            parent.manage_renameObject(id, title+'-1')
    else:  
        parent.manage_renameObject(id, title)
    context.reindexObject()
    return

@grok.subscribe(IQuestion, IObjectModifiedEvent)
def _modifyObject(context, event):
    catalog = getToolByName(context, 'portal_catalog')
    topic_officer = []
    topics = []
    if context.topic:
        brains = catalog.unrestrictedSearchResults(portal_type='ilo.qa.topic', UID=context.topic)
        for brain in brains:
            topic_officer.append(brain._unrestrictedGetObject().officer_email)
            topics.append(brain.Title)
    if topic_officer:
        context.topic_officer = ','.join(topic_officer)
    context.reindexObject()
    return

class IQuestionAddForm(dexterity.AddForm):
    grok.name('ilo.qa.question')
    template = ViewPageTemplateFile('templates/questionadd.pt')
    form.wrap(False)

    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def topic_uid(self, form_id=None):
        context = self.context
        catalog = self.catalog
        path = '/'.join(context.getPhysicalPath())
        brains = catalog.searchResults(path={'query': path, 'depth' : 1}, 
                                        portal_type='ilo.qa.topic',
                                        id = form_id)
        if brains:
            return brains[0].UID
