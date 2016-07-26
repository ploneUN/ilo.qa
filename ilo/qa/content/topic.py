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
from plone import api

from z3c.relationfield.schema import RelationChoice


# Interface class; used to define content-type schema.

class InvalidEmailAddress(ValidationError):
    "Invalid email address"

def validateaddress(value):
    try:
        checkEmailAddress(value)
    except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
    return True

class users(object):
    grok.implements(IContextSourceBinder)
    def __call__(self,context ):
        results = []
        users = context.portal_membership.listMembers()
        for user in users:
            fullname = user.getProperty('fullname')
            results.append(SimpleTerm(value=user.id, token=user.id, title=fullname))
        return SimpleVocabulary(results)

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

    officer_title = schema.TextLine(
           title=_(u"Officer Title"),
           required=True,
        )

    officer = schema.Choice(
            source=users(),
            title=u'officer',
            required=False,
        )
        


    # officer = schema.TextLine(
    #        title=_(u"Officer"),
    #        required=True,
    #     )

    # officer_email = schema.TextLine(
    #        title=_(u"Officer Email"),
    #        required=True,
    #        constraint=validateaddress,
    #     )

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
        if brain.id != context.id:
            object_Ids.append(brain.id)

    if object_Ids:
        id_number = int(max(object_Ids)) + 1
        number = '%04d' % id_number
        if len(object_Ids) > 9999:
            number = id_number
    else:
        number = '0001'
    # setattr(context, 'title', str(number))
    parent.manage_renameObject(id, str(number))
    #exclude from navigation code
    # behavior = IExcludeFromNavigation(context)
    # behavior.exclude_from_nav = True
    context.reindexObject()
    return
