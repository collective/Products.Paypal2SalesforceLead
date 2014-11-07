from zope.interface import implements
from Products.Paypal2SalesforceLead.interfaces import ISalesforceWeb2Lead

import urllib

from Products.Paypal2SalesforceLead.config import SALESFORCE_WEBTOLEAD
from Products.Paypal2SalesforceLead.config import SALESFORCE_SANDBOX_WEBTOLEAD
from Products.Paypal2SalesforceLead.config import SALESFORCE_DEFAULT_COMPANY


class SalesforceWeb2Lead(object):
    """Implements ISalesforceWeb2Lead
    """
    implements(ISalesforceWeb2Lead)
    
    def __init__(self, use_sandbox=False):
        self.urllib = urllib
        self.use_sandbox = use_sandbox
    
    def create(self, params):
        if not 'oid' in params or not 'last_name' in params:
            return False

        if not 'company' in params:
            params['company'] = SALESFORCE_DEFAULT_COMPANY
            
        params['retURL'] = 'http://www.salesforce.com'
        web2lead_url = self.use_sandbox \
            and SALESFORCE_SANDBOX_WEBTOLEAD or SALESFORCE_WEBTOLEAD

        # not so intituitively a failure will result in a returned Response
        # header of is-processed (which will include exception info)
        res = self.urllib.urlopen(web2lead_url, urllib.urlencode(params))
        success = 'is-processed' not in res.info().items() and True or False
        return success
