from zope.interface import implements
from Products.Paypal2SalesforceLead.interfaces import IPaypalIPN

import urllib
import zLOG

from Products.Paypal2SalesforceLead.config import PAYPAL_VERIFIER, PAYPAL_VERIFIER_SANDBOX

class PaypalIPN(object):
    """Implements IPaypalIPN
    """
    implements(IPaypalIPN)
    
    def __init__(self, use_sandbox = True):
        self.urllib = urllib
        self.use_sandbox = use_sandbox

    def verify(self, paypal_params):
        paypal_params['cmd'] = '_notify-validate'

        # If paypal is running in test mode, we *always* override what's in the property sheet
        paypal_declares_test_mode = paypal_params.has_key('test_ipn') and paypal_params['test_ipn'] == 1
        
        # send paypal's variables back to verify this payment
        verifier_url = (self.use_sandbox or paypal_declares_test_mode) \
                        and PAYPAL_VERIFIER_SANDBOX \
                        or PAYPAL_VERIFIER
        response = self.urllib.urlopen(verifier_url, urllib.urlencode(paypal_params)).read()
        if response != 'VERIFIED':
            zLOG.LOG('Paypal2SalesforceLead', 1, 'Payment not verified', 'Response from Paypal was "%s"' % (response))
            return False
        
        # only insert Leads for completed payments
        if not paypal_params.has_key('payment_status'):
            return False
            
        return True
