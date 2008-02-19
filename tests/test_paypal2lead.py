import os, sys

from unittest import TestCase
from zope.interface.verify import verifyClass
from mock import Mock

from Products.Paypal2SalesforceLead.interfaces import IPaypal2SalesforceLead
from Products.Paypal2SalesforceLead.paypal2lead import Paypal2SalesforceLead, InvalidPaymentException
from Products.Paypal2SalesforceLead.tests import base

class TestPaypal2Lead(TestCase):

    def setUp(self):
        self.paypal2lead = Paypal2SalesforceLead()

    def testInterface(self):
        self.failUnless(IPaypal2SalesforceLead.implementedBy(Paypal2SalesforceLead))
        self.failUnless(verifyClass(IPaypal2SalesforceLead, Paypal2SalesforceLead))

    def testCreation(self):
        self.paypal2lead.web2lead = Mock( {'create': True} )
        paypal_params = {
            'first_name': 'asdf',
            'last_name': 'asdf',
            'payer_email': 'test@example.com',
            'payment_date': '12:00:00 Sep 27, 2007 PDT',
            'mc_gross': '2.00',
        }
        
        # should raise exception if IPN verification fails
        self.paypal2lead.paypal_ipn = Mock( {'verify': False} )
        self.assertRaises(InvalidPaymentException, self.paypal2lead.create, paypal_params, 1, 1, 1, 1)        
        self.paypal2lead.paypal_ipn = Mock( {'verify': True} )

        # should raise exception if required parameters are omitted
        for k in paypal_params.keys():
            params2 = paypal_params.copy()
            del(params2[k])    
            self.assertRaises(KeyError, self.paypal2lead.create, params2, 1, 1, 1, 1)

        # given valid input and IPN verification, should return same as SalesforceWeb2Lead object
        res = self.paypal2lead.create(paypal_params, 1, 1, 1, 1)
        self.failUnless(res)
        self.paypal2lead.web2lead = Mock( {'create': False} )
        res = self.paypal2lead.create(paypal_params, 1, 1, 1, 1)
        self.failIf(res)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaypal2Lead))
    return suite
