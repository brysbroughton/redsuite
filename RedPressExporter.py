print 'redpressexporter imported'

import RedDot as red
import RedRequestObj as RRob
import RD2WXR_Definitions as wxr
import RedSession
import datetime, time

sesh = RedSession.sesh

def export(ps):
    """
    Accepts mixed list of page descriptions
    Each description is one of the following:
        1. String guid of foundation page (non-foundation pages will be ignored)
        2. Tuple of strings ([guid_page], [wordpressID_parent]) - for child pages
    """
    print "Starting export job"
    f = open('RedPressWXRExport'+str(time.time())+'.xml','w')
    f.write(wxr.header)
    for p in ps:
        if type(p) == 'string':
            exportfoundation(p)
        elif type(p) == 'tuple':
            exportfoundation(p[0], p[1]) 
        else:
            print 'unexpected page input: ' + p
    f.write(wxr.footer)
    f.close()
    
def exportfoundation(guid, wp_parent=None):
    o = RRob.RedRequestPage(guid).request()
    print o
    pass

def parse():
    pass
    
