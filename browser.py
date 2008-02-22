from zope.interface import implements
from Products import Five

from Products.CMFCore.utils import getToolByName

from Products.Paypal2SalesforceLead.interfaces import IPaypal2LeadView
from Products.Paypal2SalesforceLead.paypal2lead import Paypal2SalesforceLead

from cgi import parse_qs

class InvalidRecipientException(Exception):
    pass

class Paypal2LeadView(Five.BrowserView):
    """
    """
    implements(IPaypal2LeadView)
    
    def __init__(self, context, request):
        """
        """
        Five.BrowserView.__init__(self, context, request)

        self.properties = getToolByName(self.context, 'portal_properties')
        self.props = self.properties.paypal2lead_properties
        self.pp2sf = Paypal2SalesforceLead(self.props.use_paypal_sandbox)
    
    def __call__(self, **kw):
        """
        """
        paypal_params = self.request.form
        query_params = parse_qs(self.request['QUERY_STRING'])
        
        # fail if recipient_email not in allowed list
        props = self.props
        if paypal_params['receiver_email'] not in props.valid_recipients:
            raise InvalidRecipientException
            
        # collect the Salesforce parameters from the property sheet,
        # or from the query string if they were passed and query string overrides are allowed
        settings = {}
        for var in ('salesforce_oid', 'payment_date_field', 'payment_amount_field', 'transaction_id_field', 'item_name_field', 'lead_source', 'campaign_id'):
            try:
                settings[var] = getattr(props, var)
                if props.allow_query_string_override and query_params.has_key(var):
                    settings[var] = query_params[var][0]
            except AttributeError:
                if var not in ['campaign_id', 'transaction_id_field', 'item_name_field']:
                    raise ValueError, "You must specify a value for '%s'" % (var)
                settings[var] = None

        res = self.pp2sf.create(paypal_params, settings['salesforce_oid'], settings['payment_date_field'],
            settings['payment_amount_field'], settings['lead_source'], settings['transaction_id_field'],
            settings['item_name_field'], settings['campaign_id'])

        # send an e-mail to the payment recipient if the web-to-lead creation failed
        if not res:
            subj = 'Error creating Salesforce lead from Paypal transaction'
            from_addr = self.context.email_from_address
            to_addr = paypal_params['receiver_email']
            msg = """
Paypal verified this transaction as a valid payment, but we were unable
to add it as a Lead in Salesforce via the web-to-lead form.

Salesforce configuration:
%s

Paypal variables:
%s
""" % (settings, paypal_params)

            mailhost = self.context.MailHost
            mailhost.send(msg, to_addr, from_addr, subj)

        return True