Description

	Paypal provides a service called Instant Payment Notification (IPN) which can
	notify a URL when a payment is made.  Paypal2SalesforceLead is a very simple
	Product for Plone which sets up a listener for IPN, and adds a new Lead
	to a Salesforce.com account using a Salesforce web-to-lead form whenever a new
	payment is made.
	
	See https://www.paypal.com/us/cgi-bin/webscr?cmd=p/xcl/rec/ipn-intro-outside
	for more background on Paypal IPN.


Who's This For?

	This Product is intended for non-profit organizations that are already using
	Paypal to collect donations and Salesforce.com for CRM, but need a way to
	integrate the two.  On its own, Paypal is a reasonable option for such organizations
	to raise money on the web, because it's simple and ongoing costs are nil.  However,
	without using IPN it is difficult to collect contact information and maintain ongoing
	relationships with customers.  Using this Product to receive this information and
	store it in Salesforce.com helps address this need.
	
	Paypal2SalesforceLead is also intended for use by integrators who are setting up
	Plone and Salesforce.com for multiple clients.  A single installation of this Product
	can be used to handle multiple Paypal and Salesforce.com accounts, so that
	configuration for new customers is minimized.

    Requires Plone 2.5 or greater.  (Tested in 2.5 and 3.0)


Installation

    Place Paypal2SalesforceLead in the Products directory of your Zope instance
    and restart the server.

    Go to the 'Site Setup' page in the Plone interface and click on the
    'Add/Remove Products' link.

    Choose Paypal2SalesforceLead (check its checkbox) and click the 'Install' button.

    You may have to empty your browser cache to see the effects of the
    product installation/uninstallation.

    Uninstall: This can be done from the same management screen.


Configuration

	Paypal2SalesforceLead has a number of required settings.  At the moment these
	settings are found in a property sheet in the ZMI, called paypal2lead_properties.
	
	Navigate to http://path/to/plone/portal_properties/paypal2lead_properties/manage_workspace
	
	Configure the following settings:
	
	    * use_paypal_sandbox: Controls whether Paypal2SalesforceLead verifies payments
	        against the 'sandbox' or real versions of Paypal.  The sandbox is used by default.
	    * valid_recipients: List of e-mail addresses that are authorized to receive payment.
	        (to prevent abuse of this product)  Enter one per line.
	    * allow_query_string_override: If enabled, the remaining settings can be specified in
	        the query string of the URL entered into Paypal.  (This allows using one instance of
	        Paypal2SalesforceLead to handle notifications for many Paypal and Salesforce.com
	        instances.)
	        
	The following settings can be set on the property sheet, or in the query string of the URL
	entered into Paypal (if allow_query_string_override is enabled):
	        
	    * salesforce_oid: ID of the Salesforce instance that will be used.
    	* payment_date_field: ID of the custom payment date field on the Lead
    	* payment_amount_field: ID of the custom payment amount field on the Lead
    	* transaction_id_field: ID of the custom transaction ID field on the Lead
		* lead_source: a value to be entered for the lead_source field (optional)
		* campaign_id: a value to be entered for the Campaign_ID field (optional; no default)

Salesforce.com Configuration

	Paypal2SalesforceLead requires fields on the Lead object in Salesforce to hold the
	following data: payment amount, payment date, and transaction ID.  Create these fields.
	
	A web-to-lead form must be enabled.  To do this, click on Setup at the top of the screen in
	Salesforce.  Click on Customize under App Setup on the left sidebar, then Leads, then
	Web-to-Lead.  Click the Edit button, check the 'Web-to-Lead Enabled' checkbox, and click the
	Save button.
	
	We will also need to know the ID of your Salesforce instance, as well as for each of the custom
	fields you created above.  To find these, continuing from the current screen, click the
	'Create Web-to-Lead Form' button.  Add your custom fields to the list of Selected Fields.
	(The Return URL setting is irrelevant.)  Click the Generate button and examine the resulting
	HTML to find the value of the hidden 'oid' field, as well as the name of each of the custom
	fields.

Paypal Configuration

	Paypal must be told to perform IPN, and it must be told what URL to notify.

	From the Paypal business account, click on the Profile sub-tab.  Click on 'Instant
	Payment Notification Preferences' in the Selling Preferences column.  Here you can
	turn on IPN and specify a URL.
		
	(Another option is to add a hidden field called 'notify_url' to the form that submits
	to Paypal.  This allows the notification URL to be configured on a per-form basis.)
	
	The listener should be called as paypal2lead in the context of the Plone site in which it is
	installed.  The full URL will look something like this:
	    http://example.com/plone_site/paypal2lead
	
	You should now be able to make a test payment to your Paypal account, and see a new lead
	appear in Salesforce as a result!

	Remember to turn off the use_paypal_sandbox setting on the paypal2lead property sheet
	when you are done testing!  Otherwise all your attempted IPN verifications will fail.


Written by

    * David Glick (davidglick@onenw.org)
