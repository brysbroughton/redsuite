import RedDot as red
import RedRequestObj as RRob
import RedPressExporter as rp
import RedSession
import xml.etree.ElementTree as ET

print 'redadmin imported'

sesh = RedSession.sesh

def allfollowing(guid):
    """
    Takes guid of a RedDot foundation page.
    Recursivley descends on RedDot tree.
    Returns list of all foundation page guids following input page.
    """
    childs = []
    visited_guids = []
    
    def rec_allfollowing(guid):
        print "evaluating page "+guid
        if guid in visited_guids:
            print 'Warning: recursive link detected '+guid
            return
        visited_guids.append(guid)

        p = RRob.RedRequestPage(guid)
        p.request()
        template = p.fetch(".//PAGE[@templatetitle]",'templatetitle')[0]
        if template in red.RD_Foundation_Pages:
            childs.append(guid)
            
        lres = ET.fromstring(p.redResponse)
        ls = lres.findall('.//LINK')#ET nodes
        for l in ls:
            if l.attrib['islink'] == '1' or l.attrib['islink'] == '2':#see link type codes in RD docs
                l = l.attrib['guid']
            else:#skip references and empty links
                continue
            print "Looking for pages under "+l
            l = RRob.RedRequestLink(l)
            l.request()
            subps = l.fetch('.//PAGE','guid')
            if subps is None: continue
            for subp in subps:
                print 'checking subp '+subp
                sp = RRob.RedRequestPage(subp)
                sp.request()
                mainlink = sp.fetch('.//MAINLINK', 'pageguid')[0]
                subtemplate = sp.fetch('.//PAGE[@templatetitle]','templatetitle')[0]
                if mainlink == guid:
                    rec_allfollowing(subp)
                else:
                    print 'Strange page '+subp

    p = RRob.RedRequestPage(guid)
    p.request()
    template = p.fetch(".//PAGE[@templatetitle]",'templatetitle')[0]
    if template in red.RD_Foundation_Pages:
            rec_allfollowing(guid)

    try:
        childs.remove(guid)#don't return input guid as a child of itself
    except ValueError:
        #it wasn't in the list anyway
        pass
    return childs
