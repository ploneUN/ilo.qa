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

from zope.schema import ValidationError
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFDefault.exceptions import EmailAddressInvalid
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.app.container.interfaces import IObjectAddedEvent
from Products.CMFCore.utils import getToolByName


# Interface class; used to define content-type schema.

class InvalidEmailAddress(ValidationError):
    "Invalid email address"

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

class ITopic(form.Schema, IImageScaleTraversable):
    """
    Topic
    """

    # topic_id = schema.TextLine(
    #        title=_(u"ID"),
    #        required=True,
    #     )

    title = schema.TextLine(
           title=_(u"Topic"),
           required=True,
        )

    officer = schema.TextLine(
           title=_(u"Officer"),
           required=True,
        )

    officer_email = schema.TextLine(
           title=_(u"Officer Email"),
           required=True,
           constraint=validateaddress,
        )

    pass

alsoProvides(ITopic, IFormFieldProvider)


@grok.subscribe(ITopic, IObjectAddedEvent)
def _createObject(context, event):
    parent = context.aq_parent
    id = context.getId()
    object_Ids = []
    catalog = getToolByName(context, 'portal_catalog')
    path = '/'.join(context.aq_parent.getPhysicalPath())
    brains = catalog.unrestrictedSearchResults(path={'query': path, 'depth' : 1}, portal_type='ilo.qa.topic')
    for brain in brains:
        object_Ids.append(brain.id)

    number = ("%04d") % len(object_Ids)
    if len(object_Ids) > 1000:
      number = len(object_Ids)
    parent.manage_renameObject(id, str(number))
    #exclude from navigation code
    # behavior = IExcludeFromNavigation(context)
    # behavior.exclude_from_nav = True
    context.reindexObject()
    return
