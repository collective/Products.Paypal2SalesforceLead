from zope.interface import implements

from Products.Paypal2SalesforceLead.interfaces import IPaypal2SalesforceLead
from Products.Paypal2SalesforceLead.paypal_ipn import PaypalIPN
from Products.Paypal2SalesforceLead.salesforce_web2lead import SalesforceWeb2Lead

from time import strftime
from dateutil import parser


class InvalidPaymentException(Exception):
    pass

class Paypal2SalesforceLead(object):
    """Implements IPaypal2SalesforceLead
    """
    implements(IPaypal2SalesforceLead)

    def __init__(self, use_pp_sandbox=True, use_sf_sandbox=False):
        """
        """
        self.paypal_ipn = PaypalIPN(use_pp_sandbox)
        self.web2lead = SalesforceWeb2Lead(use_sf_sandbox)

    def create(self, paypal_params, oid, payment_date_field, 
               payment_amount_field, lead_source='Paypal', 
               transaction_id_field=None, item_name_field=None, 
               campaign_id=None):
        """
        """
        if not self.paypal_ipn.verify(paypal_params):
            raise InvalidPaymentException("Failed PayPal's verification process.")

        # A lot can go wrong here, and we want to raise a custom exception so 
        # the view class can catch it.
        try:
            # required parameters
            s_params = {
                'oid':                  oid,
                'first_name':           paypal_params['first_name'],
                'last_name':            paypal_params['last_name'],
                'email':                paypal_params['payer_email'],
                'company':              (paypal_params.has_key('payer_business_name') and paypal_params['payer_business_name'] or '[not provided]'),
                'lead_source':          lead_source,}
                
            
            # optional parameters with field names
            if transaction_id_field:
                s_params[transaction_id_field] = paypal_params['txn_id']

            if item_name_field:
                s_params[item_name_field] = paypal_params['item_name']

            if payment_date_field:
                # ignore timezones. It's up to the user to make sure that 
                # PayPal is set to use the same time zone for IPNs on the 
                # account as is set for the Salesforce org.
                # use datetutil for better parsing than strptime
                # e.g., PayPal's IPN simulator reverses order of month and day
                # in payment date compared to payment date in actual IPN.
                paydt = parser.parse(paypal_params['payment_date'])
                s_params[payment_date_field] = paydt.strftime('%m/%d/%Y')
            
            if payment_amount_field:
                s_params[payment_amount_field] = paypal_params['mc_gross']
        
        except Exception, e:
            raise InvalidPaymentException("Error extracting transaction data: %s" % e)
        
        # standard parameters that paypal *might* pass us
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
