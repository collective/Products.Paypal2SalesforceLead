from zope.interface import Interface

class IPaypal2LeadView(Interface):
    """Browser view for accessing the Paypal 2 Lead functionality
    """

class IPaypalIPN(Interface):
    """Interface for verifying Paypal payment information
    """
    def verify(paypal_params):
        """Verifies a payment notification with Paypal.  Returns True if the payment is valid
        and completed, or False if not.
        
        paypal_params should be a dictionary of the variables that were POSTed by Paypal to this request.
        """

class ISalesforceWeb2Lead(Interface):
    """Interface for inserting a new Lead in a salesforce.com account using
    a web-to-lead form.
    """
    
    def create(params):
        """Creates a new Lead.  Returns a boolean indicating whether the creation was
        successful.
        
        params is a dictionary of fields to set on the new Lead, plus an 'oid' field
        which specifies the Salesforce instance.  The 'oid' and 'last_name' keys are
        required, at the very least.
        """
        
class IPaypal2SalesforceLead(Interface):
    """Interface for converting Paypal IPN payment information into corresponding
    Salesforce.com Lead fields
    """
    
    def create(paypal_params, oid, payment_date_field, payment_amount_field, transaction_id_field, lead_source = 'Paypal', campaign_id = None):
        """Creates a new Lead in Salesforce upon successful Paypal IPN verification.
        Returns a boolean indicating whether the creation was successful.
        Raises an InvalidPaymentException if payment verification fails.
        
        paypal_params is a dictionary of the POST variables received from Paypal
        oid specifies the Salesforce instance
        payment_date_field, payment_amount_field, and transaction_id_field are the IDs
           of custom Lead fields to store payment information
        lead_source and campaign_id specify the hard-coded values for the corresponding Lead fields
        """

