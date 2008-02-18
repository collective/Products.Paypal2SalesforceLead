import os, sys

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase

ZopeTestCase.installProduct('Paypal2SalesforceLead')
PRODUCTS = ['Paypal2SalesforceLead']
PloneTestCase.setupPloneSite(products=PRODUCTS)

class TestProductUnInstallation(PloneTestCase.PloneTestCase):
    """ Ensure that our policy product installs and 
        correctly configures our portal.
    """
    def afterSetUp(self):
        self.properties = self.portal.portal_properties
        self.qi         = self.portal.portal_quickinstaller
        
        # uninstall our product
        if self.qi.isProductInstalled('Paypal2SalesforceLead'):
            self.qi.uninstallProducts(products=['Paypal2SalesforceLead',])
    
    def testPropertySheetRemoved(self):
        self.failIf("paypal2lead_properties" in self.properties.objectIds())
    
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductUnInstallation))
    return suite
