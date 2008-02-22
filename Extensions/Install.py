from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from Products.Paypal2SalesforceLead import HAS_PLONE25, HAS_PLONE30

def install(self):
    out = StringIO()

    # We install our product by running a GS profile.  We use the old-style Install.py module 
    # so that our product works w/ the Quick Installer in Plone 2.5.x
    print >> out, "Installing Paypal2SalesforceLead"
    setup_tool = getToolByName(self, 'portal_setup')
    if HAS_PLONE30:
        setup_tool.runAllImportStepsFromProfile(
            'profile-Products.Paypal2SalesforceLead:default',
            purge_old=False)
    else:
        old_context = setup_tool.getImportContextID()
        setup_tool.setImportContext('profile-Products.Paypal2SalesforceLead:default')
        setup_tool.runAllImportSteps()
        setup_tool.setImportContext(old_context)
    print >> out, "Successfully installed Paypal2SalesforceLead."
    return out.getvalue()

def uninstall(self):
    out = StringIO()

    # remove our property sheet
    propsTool = getToolByName(self, 'portal_properties')
    propsTool.manage_delObjects(['paypal2lead_properties'])

    print >> out, "\nSuccessfully uninstalled Paypal2SalesforceLead."
    return out.getvalue()
