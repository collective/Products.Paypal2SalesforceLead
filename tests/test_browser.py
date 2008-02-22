import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from mock import Mock, expectException

from Products.Paypal2SalesforceLead.browser import Paypal2LeadView, InvalidRecipientException
from Products.Paypal2SalesforceLead.paypal2lead import InvalidPaymentException
from Products.Paypal2SalesforceLead.tests import base

ZopeTestCase.installProduct('Paypal2SalesforceLead')
PRODUCTS = ['Paypal2SalesforceLead']
PloneTestCase.setupPloneSite(products=PRODUCTS)

class TestPaypal2LeadView(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.view = self.folder.restrictedTraverse('paypal2lead')
        
        self.portal.MailHost = base.MailHostMock('MailHost')
        self.mailhost = self.portal.MailHost
        self.view.context.email_from_address = 'admin@example.com'
        
        self.properties = self.portal.portal_properties
        props = self.properties.paypal2lead_properties
        props.valid_recipients = ['me@example.com']
        props.allow_query_string_override = False
        props.salesforce_oid = 1
        props.payment_date_field = 1
        props.payment_amount_field = 1

    def testEmailOnFailure(self):
        # make sure that payment recipient will get an e-mail if the web-to-lead
        # creation fails
        self.view.pp2sf = Mock( {'create': False} )
        self.view.request.form['receiver_email'] = 'me@example.com'
        self.view.request['QUERY_STRING'] = 'salesforce_oid=1&payment_date_field=1&payment_amount_field=1'
        self.view()
        self.assertEqual(self.mailhost.n_mails, 1)
        self.assertEqual(self.mailhost.mto, 'me@example.com')
        self.assertEqual(self.mailhost.mfrom, self.view.context.email_from_address)
        
        # make sure that no e-mail is sent if the paypal verification was invalid
        self.view.pp2sf = Mock()
        self.view.pp2sf.mockSetExpectation('create', expectException(InvalidPaymentException))
        self.assertRaises(InvalidPaymentException, self.view)
        self.assertEqual(self.mailhost.n_mails, 1)

    def testRejectInvalidRecipientEmail(self):
        self.view.pp2sf = Mock( {'create': True} )
        
        # make sure that we only handle payments to specified recipients (to prevent DOSing)
        self.view.request.form['receiver_email'] = 'invalid@example.com'
        self.view.request['QUERY_STRING'] = 'salesforce_oid=1&payment_date_field=1&payment_amount_field=1'
        self.assertRaises(InvalidRecipientException, self.view)
        
        # make sure that valid payments go through
        self.view.request.form['receiver_email'] = 'me@example.com'
        self.failUnless(self.view())

    def testQueryStringParameterOverride(self):
        self.view.pp2sf = Mock( {'create': True} )
        self.view.request.form['receiver_email'] = 'me@example.com'
        props = self.properties.paypal2lead_properties
        
        # make sure that things succeed if a required parameter is specified only on the query string
        props.salesforce_id = None
        props.allow_query_string_override = True
        self.view.request['QUERY_STRING'] = 'salesforce_oid=1'
        self.failUnless(self.view())
        
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaypal2LeadView))
    return suite

if __name__ == '__main__':
    framework()
