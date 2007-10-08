class UrllibMock(object):
    """
    mock up an HTTP request/response so that we can run our tests
    without worrying about having an actual connection
    """
    def __init__(self, response):
        self.response = response

    def urlopen(self, url, params = ''):
        return UrllibResponseMock(self)
        
class UrllibResponseMock(object):
    """
    urllib's urlopen() returns a response object, which this mocks
    """
    def __init__(self, request):
        self.response = request.response
    
    def read(self):
        return self.response

from Products.SecureMailHost.SecureMailHost import SecureMailHost as Base

class MailHostMock(Base):
    """
    mock up the send method so that emails do not actually get sent
    during unit tests we can use this to verify that the notification
    process is still working as expected
    """
    def __init__(self, id):
        Base.__init__(self, id, smtp_notls=True)
        self.mail_text = ''
        self.n_mails = 0
        self.mto = ''
        self.mfrom = ''
        self.subject = ''
    def send(self, mail_text, full_to_address, full_from_address, subject):
        self.mail_text = mail_text
        self.mto = full_to_address
        self.mfrom = full_from_address
        self.subject = subject
        self.n_mails += 1
