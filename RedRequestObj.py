print 'RedRequestObj imported'

import RedDot as red
import xml.etree.ElementTree as ET
import xml, httplib, urllib


class RedRequestObj(object):
    """
    To be exended by specific request type classes
    """

    guid = None
    redResponse = None
    RQL = None
    
    def __init__(self, guid_in=None):
        if guid_in is not None:
            self.guid = guid_in

    @staticmethod
    def getXpath(xml, path):
        try:
            node = ET.fromstring(xml)
            ns = node.findall(path)
            return ns
        except xml.parsers.expat.ExpatError:
            print 'invalid xml\n' + xml
            raise
        
    def fetch(self, path, attr=None, limit=None):
        elems = self.getXpath(self.redResponse, path)
        if len(elems) == 0:
            print 'Error: elements not found: ' + path
            return
        if attr is None:
            elems = map(lambda x:x.tag, elems)
        else:
            elems = map(lambda x:x.attrib[attr], elems)
        if limit is not None:
            elems = elems[0:limit]
        return elems

    def request(self, padded=False):
        #implement cacheing later - this is non-cached case
        conn = httplib.HTTPSConnection(red.host)
        params = urllib.urlencode({'RQL': self.RQL})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/x-ms-application,", "Connection": "Keep-Alive", "POST": params}
        try:
            conn.request('POST', red.aspconnecturl, params, headers)
            self.redResponse = conn.getresponse().read()
            self.err()
            return self.redResponse
        except Exception as ex:
            raise ex

    def setguid(self, guid_in):
        self.guid = guid_in

    def getguid(self):
        return self.guid

    def setrql(self, rql):
        self.RQL = rql

    def getrql(self):
        return self.RQL
    
    def err(self):
        if self.redResponse is None:
            print 'No response received from RedDot'
        else:
            try:
                node = ET.fromstring(self.redResponse)
                if node.tag == 'ERROR':
                    errcode = node.text.upper()
                    if red.RD_Error_Messages.has_key(errcode):
                        print red.RD_Error_Messages[errcode]
                    else:
                        print errcode
                else:
                    pass
                    #print 'Unknown Error>>>\n' + self.redResponse
            except xml.parsers.expat.ExpatError:
                print 'RedDot returned invalid xml:\n' + self.redResponse
                pass


class RedRequestLink(RedRequestObj):

    RQL = '<LINK guid="!!!" action="load"><PAGES action="list" /><URL action="load" /></LINK>'



class RedRequestPage(RedRequestObj):

    RQL = '<PAGE guid="!!!" action="load" />'
    
    
class RedRequestElement(RedRequestObj):
    
    RQL = '!!!'
    
    
class RedRequestText(RedRequestObj):
    
    RQL = '!!!'


class RedRequestReference(RedRequestObj):

    RQL = '!!!'

    
