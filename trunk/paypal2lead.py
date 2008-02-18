from zope.interface import implements

from Products.Paypal2SalesforceLead.interfaces import IPaypal2SalesforceLead
from Products.Paypal2SalesforceLead.paypal_ipn import PaypalIPN
from Products.Paypal2SalesforceLead.salesforce_web2lead import SalesforceWeb2Lead

from time import strftime, strptime

class InvalidPaymentException(Exception):
    pass

class Paypal2SalesforceLead(object):
    """Implements IPaypal2SalesforceLead
    """
    implements(IPaypal2SalesforceLead)
    
    def __init__(self, use_sandbox = True):
        """
        """
        self.paypal_ipn = PaypalIPN(use_sandbox)
        self.web2lead = SalesforceWeb2Lead()
    
    def create(self, paypal_params, oid, payment_date_field, payment_amount_field, transaction_id_field, lead_source = 'Paypal', campaign_id = None):
        """
        """
        
        if not self.paypal_ipn.verify(paypal_params):
            raise InvalidPaymentException
        
        # required parameters
        s_params = {
            'oid':                  oid,
            'first_name':           paypal_params['first_name'],
            'last_name':            paypal_params['last_name'],
            'email':                paypal_params['payer_email'],
            'company':              (paypal_params.has_key('payer_business_name') and paypal_params['payer_business_name'] or '[not provided]'),
            'lead_source':          lead_source,
            payment_date_field:     strftime('%m/%d/%Y', strptime(paypal_params['payment_date'], '%H:%M:%S %b %d, %Y %Z')),
            payment_amount_field:   paypal_params['mc_gross'],
            transaction_id_field:   paypal_params['txn_id'],
        }

        # parameters that paypal *might* pass us
        key_mapping = {
            'address_city': 'city',
            'address_state': 'state',
            'contact_phone': 'phone',
            'address_street': 'street',
            'address_zip': 'zip',
            'address_country': 'country',
            'memo': 'description',
        }
        for paypal_key, salesforce_key in key_mapping.items():
            if paypal_params.has_key(paypal_key):
                s_params[salesforce_key] = paypal_params[paypal_key]
                
        if campaign_id:
            s_params['Campaign_ID'] = campaign_id

        return self.web2lead.create(s_params)