from collective.grok import gs
from ilo.qa import MessageFactory as _

@gs.importstep(
    name=u'ilo.qa', 
    title=_('ilo.qa import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('ilo.qa.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
