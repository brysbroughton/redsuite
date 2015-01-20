print 'RedRequestObj imported'

import RedDot as red
import xml.etree.ElementTree as ET
import xml, httplib, urllib
import pprint

loginguid=''
sessionkey=''

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
        #print 'getXpath:'
        #pprint.pprint(xml)
        #pprint.pprint(path)
        try:
            node = ET.fromstring(xml)
            ns = node.findall(path)
            return ns
        except xml.parsers.expat.ExpatError:
            print 'invalid xml\n'# + xml
            raise
        
    def fetch(self, path, attr=None, limit=None):
        elems = self.getXpath(self.redResponse, path)
        if len(elems) == 0:
            print 'Warning: elements not found: ' + path
            return
        if attr is None:
            elems = map(lambda x:x.tag, elems)
        else:
            #pprint.pprint(elems[0].attrib)
            try:
                elems = map(lambda x:x.attrib[attr], elems)
            except KeyError:
                #raise Exception(path + ' has no attribute called '+attr)
                pass
        if limit is not None:
            elems = elems[0:limit]
        return elems

    def request(self, nocache=False):
        if nocache:
            print 'no cache'
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
        else:
            if red.cached(self.getguid()):
                self.redResponse = red.getcached(self.getguid())
                return self.redResponse
            else:
                print 'new request'
                conn = httplib.HTTPSConnection(red.host)
                params = urllib.urlencode({'RQL': self.RQL})
                headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/x-ms-application,", "Connection": "Keep-Alive", "POST": params}
                try:
                    conn.request('POST', red.aspconnecturl, params, headers)
                    self.redResponse = conn.getresponse().read()
                    self.err()
                    red.cache(self.getguid(), self.redResponse)
                    return self.redResponse
                except Exception as ex:
                    raise ex

    def setguid(self, guid_in):
        self.guid = guid_in

    def getguid(self):
        return self.guid

    def setrql(self, rql, padded=False):
        if not padded:
            self.RQL = '<IODATA loginguid="'+loginguid+'" sessionkey="'+sessionkey+'">'+rql+'</IODATA>'
        else:
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
                        raise Exception( red.RD_Error_Messages[errcode] )
                    else:
                        raise Exception( errcode )
                else:
                    pass
                    #print 'Unknown Error>>>\n' + self.redResponse
            except Exception as ex:
                print 'Warning: RedDot returned invalid xml:\n' + self.redResponse
                pass


class RedRequestLink(RedRequestObj):

    def __init__(self, guid_in=''):
        RedRequestObj.__init__(self, guid_in)
        self.setrql('<LINK guid="'+self.getguid()+'" action="load"><PAGES action="list" /><URL action="load" /></LINK>')

    
class RedRequestPage(RedRequestObj):

    def __init__(self, guid_in=''):
        RedRequestObj.__init__(self, guid_in)
        self.setrql('<PAGE guid="'+self.getguid()+'" action="load" option="extendedinfo" /><PAGE guid="'+self.getguid()+'"><ELEMENTS action="load" /><LINKS action="load" /></PAGE>')
    
    
class RedRequestElement(RedRequestObj):
    
    def __init__(self, guid_in=''):
        RedRequestObj.__init__(self, guid_in)
        self.setrql('<ELT guid="'+self.getguid()+'" action="load" subelements="1"><SELECTIONS action="list" /></ELT>')
        #if has attr 'referenceelementguid' - must follow guid
        #issue folder request on 'eltsrcsubdirguid' to get path
    
    
class RedRequestText(RedRequestObj):

    def __init__(self, guid_in=''):
        RedRequestObj.__init__(self, guid_in)
        self.setrql('<IODATA loginguid="'+loginguid+'" sessionkey="'+sessionkey+'" format="1"><PROJECT><TEXT action="load" guid="'+self.getguid()+'" texttype="1" /></PROJECT></IODATA>', True)


class RedRequestFolder(RedRequestObj):

    def __init__(self, guid_in=''):
        RedRequestObj.__init__(self, guid_in)
        self.setrql('<PROJECT><FOLDER action="load" guid="'+self.getguid()+'" /></PROJECT>')


class RedRequestReference(RedRequestObj):

    def __init__(self, guid_in=''):
        RedRequestObj.__init__(self, guid_in)
        self.setrql('<TREESEGMENT action="gototreereference" guid="'+self.getguid()+'" type="link" />')


    
