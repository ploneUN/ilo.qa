from zope.interface import Interface
from z3c.form import button

class IProductSpecific(Interface):
    pass

class IButtonsSend(Interface):
    save = button.Button(title=u"Send")
    cancel = button.Button(title=u"Cancel")

