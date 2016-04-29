from five import grok
from plone.directives import dexterity, form
from ilo.qa.content.answer import IAnswer
from ilo.qa.content.qa_facility import IQAFacility
from Products.CMFCore.utils import getToolByName
from plone import api
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


grok.templatedir('templates')

class email_officer(dexterity.DisplayForm):
    grok.context(IQAFacility)
    grok.require('zope2.View')
    
    
    @property
    def catalog(self):
        return getToolByName(self.context, 'portal_catalog')
    
    def get_officer(self):
        results = {'officer':'', 'officer_email':''}
        if self.request:
            form = self.request.form
            if 'id' in form:
                brains = self.catalog.unrestrictedSearchResults(portal_type='ilo.qa.topic', UID=form['id'])
                for brain in brains:
                    obj =  brain._unrestrictedGetObject()
                    results['officer'] = obj.officer
                    results['officer_email'] = obj.officer_email
        return results
    
    def send_email(self):
        if self.get_officer()['officer']:
            if self.request:
                form = self.request.form
                if 'email_subject' in form and 'email_message' in form:
                    mail = self.context.MailHost
                    from_email = api.user.get_current().getProperty('email')
                    from_name = api.user.get_current().getProperty('fullname')
                    msg = {}
                    msg['From'] = '%s' % from_email
                    msg['To'] = '%s' % self.get_officer()['officer_email']
                    msg['Subject'] = form['email_subject']
                    msg['Message'] = form['email_message']
                    mailhost = self.context.MailHost
                    try:
                        mailhost.send(msg['Message'], mto=msg['To'], mfrom=msg['From'], subject=msg['Subject'], immediate=True, charset='utf8', msg_type=None)
                        self.context.plone_utils.addPortalMessage(u"Email successfully sent", 'success')
                        self.request.RESPONSE.redirect(self.context.absolute_url())
                    except:
                        self.context.plone_utils.addPortalMessage(u"Unable to send email", 'info')
                        self.request.RESPONSE.redirect(self.context.absolute_url())
        return ''
                    
                    
                   