from zope.interface import implements
from Products.Paypal2SalesforceLead.interfaces import ISalesforceWeb2Lead

import urllib

from Products.Paypal2SalesforceLead.config import SALESFORCE_WEBTOLEAD, SALESFORCE_DEFAULT_COMPANY

class SalesforceWeb2Lead(object):
    """Implements ISalesforceWeb2Lead
    """
    implements(ISalesforceWeb2Lead)
    
    def __init__(self):
        self.urllib = urllib
    
    def create(self, params):
        if not params.has_key('oid') or not params.has_key('last_name'):
            return False

        if not params.has_key('company'):
            params['company'] = SALESFORCE_DEFAULT_COMPANY
            
        params['retURL'] = 'http://www.salesforce.com'
        res = self.urllib.urlopen(SALESFORCE_WEBTOLEAD, urllib.urlencode(params)).read()
        success = (res.find("window.location.replace(url + escapedHash);") > -1)
        return success
