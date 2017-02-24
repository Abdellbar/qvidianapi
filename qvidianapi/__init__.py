import zeep
import logging.config
from lxml import etree
import sys
from HTMLParser import HTMLParser

QvidianAuthenticationWSDL = './wsdl/QvidianAuthentication.wsdl'
CommonWSDL ='./wsdl/Common.wsdl'
ContentLibraryWSDL='./wsdl/ContentLibrary.wsdl'

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(name)s: %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'zeep.transports': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
})

class MyHTMLParser(HTMLParser):
	def __init__(self):
		self.text = ''
		self.start = False
		self.end   = False
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		if ( not self.end):
			if  (tag == 'div') :
				self.start = True

	def handle_endtag(self, tag):
		if ( not self.end):
			if  (tag == 'div') :
				self.end = True

	def handle_data(self, data):
		if ( not self.end) and self.start :
			self.text += data

def update_endpoint(file,newurl):
	try :
		tree = etree.parse(file)
		namespaces = {'soap':'http://schemas.xmlsoap.org/wsdl/soap/'}
		tree.findall('.//soap:address',namespaces)[0].attrib['location']=newurl
		with open(file, 'w') as file_handle:
		    file_handle.write(etree.tostring(tree, pretty_print=True, encoding='utf8'))		
	except:
		e = sys.exc_info()[0]
		print e
		return False
	else:
		return True


class QvidianAuthentication:
	def __init__( self, wsdl_file, endpoint_url):
		update_endpoint(wsdl_file,endpoint_url)
		self.client = zeep.Client(wsdl=wsdl_file)
		self.ConnectResult = None
	def Connect(self, userName, password):
		self.ConnectResult = self.client.service.Connect(userName=userName, password=password)['body']['ConnectResult']

class Common:
	def __init__( self, wsdl_file, endpoint_url):
		update_endpoint(wsdl_file,endpoint_url)
		self.client = zeep.Client(wsdl=wsdl_file)
		self.HasPermissionsResponse = None
		self.HeaderType = self.client.get_element('ns0:QvidianCredentialHeader')
		
	def HasPermissions(self, AuthenticationToken , Permission):
		QvidianCredentialHeader = self.HeaderType(AuthenticationToken=AuthenticationToken)
		self.HasPermissionsResponse=self.client.service.HasPermissions(_soapheaders=[QvidianCredentialHeader],Permission=Permission)['body']

class ContentLibrary:
	def __init__( self, wsdl_file, endpoint_url):
		update_endpoint(wsdl_file,endpoint_url)
		self.client = zeep.Client(wsdl=wsdl_file)
		self.librarySearchRequestsInitResponse    = None
		self.librarySearchesAsListsResponse       = None
		self.libraryContentPreviewHTMLGetResponse = None
		self.HeaderType = self.client.get_element('ns0:QvidianCredentialHeader')

	def librarySearchRequestsInit(self, AuthenticationToken , requestCount):
		QvidianCredentialHeader = self.HeaderType(AuthenticationToken=AuthenticationToken)
		self.librarySearchRequestsInitResponse=self.client.service.librarySearchRequestsInit(_soapheaders=[QvidianCredentialHeader],requestCount=requestCount)['body']['librarySearchRequestsInitResult']		

	def librarySearchesAsLists(self, AuthenticationToken , searchRequestList):
		QvidianCredentialHeader = self.HeaderType(AuthenticationToken=AuthenticationToken)
		self.librarySearchesAsListsResponse=self.client.service.librarySearchesAsLists(_soapheaders=[QvidianCredentialHeader],searchRequestList=searchRequestList)['body']['librarySearchesAsListsResult']		

	def libraryContentPreviewHTMLGet(self, AuthenticationToken , ContentID):
		QvidianCredentialHeader = self.HeaderType(AuthenticationToken=AuthenticationToken)
		self.libraryContentPreviewHTMLGetResponse=self.client.service.libraryContentPreviewHTMLGet(_soapheaders=[QvidianCredentialHeader],contentID=ContentID,revision='-1')['body']['libraryContentPreviewHTMLGetResult']		


 













