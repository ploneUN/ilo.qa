from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.autoform.interfaces import IFormFieldProvider
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
        brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.topic',review_state='internally_published')
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

    dexteritytextindexer.searchable('topic_creator')
    form.mode(topic_creator='hidden')
    topic_creator = schema.TextLine(
           title=_(u"Topic Creator"),
           required=False,
        )
    pass

alsoProvides(IQuestion, IFormFieldProvider)


@grok.subscribe(IQuestion, IObjectAddedEvent)
def _createObject(context, event):
    catalog = getToolByName(context, 'portal_catalog')
    membership = getToolByName(context, 'portal_membership')
    topic_creators = []
    if context.topic:
        brains = catalog.unrestrictedSearchResults(portal_type='ilo.qa.topic', UID=context.topic)
        for brain in brains:
            if membership.getMemberById(brain.Creator).getProperty('email'):
                topic_creators.append(membership.getMemberById(brain.Creator).getProperty('email'))
    if topic_creators:
        context.topic_creator = ','.join(topic_creators)
    
    if membership.getMemberById(context.Creator()).getProperty('email'):
        context.question_creator = membership.getMemberById(context.Creator()).getProperty('email')
        
    context.reindexObject()
    return
