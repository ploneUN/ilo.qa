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


# Interface class; used to define content-type schema.

class IEmailTemplate(form.Schema, IImageScaleTraversable):
    """
    Email Template
    """
    send_to = schema.TextLine(
           title=_(u"Send To"),
           required=True,
        )

    send_from = schema.TextLine(
           title=_(u"Send From"),
           required=True,
        )

    email_body = schema.Text(
           title=_(u"Body"),
           required=True,
        )

    email_footer = schema.Text(
           title=_(u"Footer/Signature"),
           required=True,
        )

    pass

alsoProvides(IEmailTemplate, IFormFieldProvider)
