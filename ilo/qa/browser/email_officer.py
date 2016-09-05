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

    @property
    def membership(self):
        return getToolByName(self.context, 'portal_membership')


    def officer_details(self, officer=None):
        membership = self.membership
        name = membership.getMemberById(officer)
        email = name.getProperty('email')
        fullname = name.getProperty('fullname')
        return {'email':email,
                'fullname': fullname}

    def get_officer(self):
        results = {'officer':'', 'officer_email':''}
        if self.request:
            form = self.request.form
            if 'id' in form:
                officer = form['id']
                results['officer'] = officer
                results['officer_email'] = self.officer_details(officer)['email']
                results['fullname'] = self.officer_details(officer)['fullname']
        return results
    
    def send_email(self):
        if self.get_officer()['officer']:
            if self.request:
                form = self.request.form
                if 'email_subject' in form and 'email_message' in form:
                    mail = self.context.MailHost
                    from_email = api.user.get_current().getProperty('email')
                    from_name = api.user.get_current().getProperty('fullname')
                    #msg = {}
                    msg = MIMEMultipart()
                    
                    msg['From'] = '%s <%s>' % (from_name, from_email)
                    msg.add_header('reply-to', from_email)
                    msg['To'] = '%s' % self.get_officer()['officer_email']
                    msg['Subject'] = 'ILO QA: %s' % form['email_subject']
                    body= form['email_message'].encode('utf-8')
                    msg.attach(MIMEText(body, 'plain', 'utf-8'))
                    mailhost = self.context.MailHost
                    try:
                        #mailhost.send(msg['Message'], mto=msg['To'], mfrom=msg['From'], subject=msg['Subject'], immediate=True, charset='utf8', msg_type=None)
                        mailhost.send(msg.as_string())
                        self.context.plone_utils.addPortalMessage(u"Email successfully sent", 'success')
                        self.request.RESPONSE.redirect(self.context.absolute_url())
                    except:
                        self.context.plone_utils.addPortalMessage(u"Unable to send email", 'info')
                        self.request.RESPONSE.redirect(self.context.absolute_url())
        return ''
    
    def auth_user(self, ):
        return api.user.get_current().getProperty('email')
    
                    
                    
                   