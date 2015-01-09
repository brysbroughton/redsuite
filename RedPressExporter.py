print 'redpressexporter imported'

import RedDot as red
import RedRequestObj as RRob
import RD2WXR_Definitions as wxr
import RedSession
import datetime, time
import pprint

sesh = RedSession.sesh

def export(ps):
    """
    Accepts mixed list of page descriptions
    Each description is one of the following:
        1. String guid of foundation page (non-foundation pages will be ignored)
        2. Tuple of strings ([guid_page], [wordpressID_parent], [wordpressTitle_parent]) - for child pages
    """
    print "Starting export job"
    f = open('RedPressWXRExport'+str(time.time())+'.xml','w')
    f.write(wxr.header)
    pprint.pprint(ps)
    for p in ps:
        if type(p).__name__ == 'str':
            exportfoundation(f, p)
        elif type(p).__name__ == 'tuple':
            exportsubfoundation(f, p[0], p[1], p[2]) 
        else:
            print 'unexpected page input: ' + p
    f.write(wxr.footer)
    f.close()
    
def exportfoundation(f, guid):
    o = RRob.RedRequestPage(guid)
    o.request()
    #verify is foundation page
    if o.fetch('.//PAGE', 'templatetitle', 1)[0] not in red.RD_Foundation_Pages:
        print 'Warning: '+guid+' is not a foundation page. Nothing exported.'
        return
    

def exportsubfoundation(f, guid, parent_id, parent_title):
    """
    Exporting a subpage requires the parent page is already imported.
    Must supply exact id and title of page in wordpress.
    """

def parse():
    pass
    
