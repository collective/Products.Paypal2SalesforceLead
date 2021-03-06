from unittest import TestCase
from zope.interface.verify import verifyClass

from Products.Paypal2SalesforceLead.interfaces import ISalesforceWeb2Lead
from Products.Paypal2SalesforceLead.salesforce_web2lead import SalesforceWeb2Lead
from Products.Paypal2SalesforceLead.tests import base


class SalesforceResponseMock(object):

    def __init__(self, header_dict):
        self.header = header_dict

    def info(self):
        return self.header

    def urlopen(self, url, params):
        return self


class TestSalesforceWeb2Lead(TestCase):

    def setUp(self):
        self.w2l = SalesforceWeb2Lead()
        
    def testInterface(self):
        self.failUnless(ISalesforceWeb2Lead.implementedBy(SalesforceWeb2Lead))
        self.failUnless(verifyClass(ISalesforceWeb2Lead, SalesforceWeb2Lead))
        
    def testCreateSalesforceLead(self):
        params = {
            'oid':          'asdf',
            'last_name':    'asdf'
        }
        self.w2l.urllib = SalesforceResponseMock({})
        
        # should return true upon successful creation
        res = self.w2l.create(params)
        self.failUnless(res)
        
        # should fail if required parameters are missing
        for p in params.keys():
            params2 = params
            del(params2[p])
            res = self.w2l.create(params2)
            self.failIf(res)
            
        # should return false if web-to-lead creation fails
        self.w2l.urllib = SalesforceResponseMock({'is-processed': 
                'true Exception:common.exception.SalesforceGenericException'}
        )
        res = self.w2l.create(params)
        self.failIf(res)
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSalesforceWeb2Lead))
    return suite
