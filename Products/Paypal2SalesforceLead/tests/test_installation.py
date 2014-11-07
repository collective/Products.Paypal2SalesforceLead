from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

ZopeTestCase.installProduct('Paypal2SalesforceLead')
PRODUCTS = ['Paypal2SalesforceLead']
PloneTestCase.setupPloneSite(products=PRODUCTS)

class TestProductInstallation(PloneTestCase.PloneTestCase):
    """ Ensure that our policy product installs and 
        correctly configures our portal.
    """
    def afterSetUp(self):
        self.properties = self.portal.portal_properties
    
    def testPropertySheetAdded(self):
        self.failUnless("paypal2lead_properties" in self.properties.objectIds())
    
    def testPropertySheetMaintainsExpectedProperties(self):
        props = getattr(self.properties, 'paypal2lead_properties')
        
        for prop in ('valid_recipients', 'use_paypal_sandbox', 
                     'use_salesforce_sandbox'):
            self.failUnless(hasattr(props, prop),
                "The Paypal2SalesforceLead property sheet is not maintaining the property %s" % prop)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstallation))
    return suite
