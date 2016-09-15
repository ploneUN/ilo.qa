from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class ILOQAView(BrowserView):
    
    def stripped_answer(self):
        context = self.context
        if context.portal_type == 'ilo.qa.answer':
            if context.answer:
                return strip_tags(context.answer)
        return ''