"""

"""

from setuptools import setup, find_packages

setup(name = "Products.Paypal2SalesforceLead",
    version = "1.2.1",
    description = "Paypal provides a service called Instant Payment Notification (IPN) which can notify a URL when a payment is made.  Paypal2SalesforceLead is a very simple Product for Plone which sets up a listener for IPN, and adds a new Lead to a Salesforce.com account using a Salesforce web-to-lead form whenever a new payment is made. See https://www.paypal.com/us/cgi-bin/webscr?cmd=p/xcl/rec/ipn-intro-outside for more background on Paypal IPN.",
    author = "David Glick",
    author_email = "david@glicksoftware.com",
    url = "http://www.glicksoftware.com",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ],
    namespace_packages=['Products', ],    
    packages=find_packages(exclude=['ez_setup']),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Framework :: Zope2",        
    ],     
    license="GPL2",
    include_package_data = True,   
    zip_safe=False        
) 
