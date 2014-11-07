__import__('pkg_resources').declare_namespace(__name__)

# Check for Plone versions
try:
    from Products.CMFPlone.migrations import v2_5
except ImportError:
    HAS_PLONE25 = False
else:
    HAS_PLONE25 = True
try:
    from Products.CMFPlone.migrations import v3_0
except ImportError:
    HAS_PLONE30 = False
else:
    HAS_PLONE30 = True
