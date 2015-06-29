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
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName
from z3c.form.interfaces import IEditForm, IAddForm


# Interface class; used to define content-type schema.

class IAnswer(form.Schema, IImageScaleTraversable):
    """
    Answer
    """
    
    dexteritytextindexer.searchable('answer')
    form.widget(answer=WysiwygFieldWidget)
    answer = schema.Text(title=u"Answer")
    
    dexteritytextindexer.searchable('question_creator')
    form.mode(question_creator='hidden')
    question_creator = schema.TextLine(
           title=_(u"Question Creator"),
           required=False,
        )

    dexteritytextindexer.searchable('answer_creator')
    form.mode(answer_creator='hidden')
    answer_creator = schema.TextLine(
           title=_(u"Answer Creator"),
           required=False,
        )

    pass

alsoProvides(IAnswer, IFormFieldProvider)

def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False

@grok.subscribe(IAnswer, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    membership = getToolByName(context, 'portal_membership')
    if parent.portal_type == 'ilo.qa.question':
        creator = parent.Creator()
        if membership.getMemberById(creator).getProperty('email'):
            context.question_creator = membership.getMemberById(creator).getProperty('email')
    if membership.getMemberById(context.Creator()).getProperty('email'):
        context.answer_creator = membership.getMemberById(context.Creator()).getProperty('email')
    
    
    path = '/'.join(context.aq_parent.getPhysicalPath())
    brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.answer')
    for brain in brains:
        if brain.id != context.id and (brain.id).startswith('ans-'):
            object_Ids.append(brain.id)

    num_ids = []
    context_title = ''
    if object_Ids:
        for num in object_Ids:
            if '-' in num:
                val = num.split('-')
                if len(val) == 2:
                    if is_number(val[1]):
                        num_ids.append(int(val[1]))
        if num_ids:
            number = max(num_ids) + 1
            context_title = 'ANS - %04d' % number
            number = 'ans-%04d' % number
    else:
        number = 'ans-0001'
        context_title = 'ANS - 0001'
    
    
    #number = ("%04d") % len(object_Ids)
    #if number in object_Ids:
    #    max_number = max(object_Ids)
    #    
    #else:
    #    if len(object_Ids) > 1000:
    #      number = len(object_Ids)
    setattr(context, 'title', context_title)
    parent.manage_renameObject(id, str(number))
    #exclude from navigation code
    # behavior = IExcludeFromNavigation(context)
    # behavior.exclude_from_nav = True
    context.reindexObject()
    return
