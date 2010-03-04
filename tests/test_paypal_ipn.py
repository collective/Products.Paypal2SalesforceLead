import os, sys

from unittest import TestCase
from zope.interface.verify import verifyClass

from Products.Paypal2SalesforceLead.interfaces import IPaypalIPN
from Products.Paypal2SalesforceLead.paypal_ipn import PaypalIPN
from Products.Paypal2SalesforceLead.tests import base

class TestPaypalIPN(TestCase):

    def setUp(self):
        self.paypal_ipn = PaypalIPN()

    def testInterface(self):
        self.failUnless(IPaypalIPN.implementedBy(PaypalIPN))
        self.failUnless(verifyClass(IPaypalIPN, PaypalIPN))

    def testPaypalIPNResponses(self):
        # should return false if IPN verification fails
        self.paypal_ipn.urllib = base.UrllibMock('INVALID')
        res = self.paypal_ipn.verify({})
        self.failIf(res)
        
        # should return false if IPN verification succeeds but payment_status is not set
        self.paypal_ipn.urllib = base.UrllibMock('VERIFIED')
        res = self.paypal_ipn.verify({})
        self.failIf(res)
        
        # should succeed if IPN verification succeeds, regardless of payment_status
        possible_status_vals = ('Canceled_Reversal',
                                'Completed',
                                'Created',
                                'Denied',
                                'Expired',
                                'Failed',
                                'Pending',
                                'Processed',
                                'Reversed',
                                'Refunded',
                                'Voided')
        for stat in possible_status_vals:
            res = self.paypal_ipn.verify({'payment_status': stat})
            self.failUnless(res, "verify() failed for status %s" % stat)
    

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPaypalIPN))
    return suite
