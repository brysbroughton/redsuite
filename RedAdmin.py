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
        try:
            template = p.fetch(".//PAGE[@templatetitle]",'templatetitle')[0]
        except TypeError:
            #Occurs when no templatetitle = not a content page
            return
            pass
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
                mainlink = sp.fetch(".//LINK[@ismainlink='1']", 'pageguid')[0]
                try:
                    subtemplate = sp.fetch('.//PAGE[@templatetitle]','templatetitle')[0]
                except TypeError:
                    #Occures when no template title = not a content page
                    continue
                    pass
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


def allinpub(guid):
    """
    Takes guid of a foundation page.
    Returns list of all guids of foundation pages with the same publication package.

    <IODATA loginguid="[!guid_login!]" sessionkey="[!key!]">
      <PROJECT>
        <EXPORTPACKET guid="[!guid_exportpacket!]">
          <REFERENCES action="list" />
        </EXPORTPACKET>
      </PROJECT>
    </IODATA>
        
    """
    return_guids = []
    #load page info
    p = RRob.RedRequestPage(guid)
    pres = p.request()
    try:
        template = p.fetch(".//PAGE[@templatetitle]",'templatetitle')[0]
        if template not in red.RD_Foundation_Pages:
            raise Exception("Input must be guid of foundation page")
    except TypeError:
        print "Must be a foundation page!"
        raise
    #get mainlink guid
    main_link = p.fetch(".//LINK[@ismainlink='1']", 'guid')[0]
    
    #load exportpacket of mainlink guid
    e = RRob.RedRequestObj()
    e.setrql("""  <PROJECT>
    <EXPORTPACKET action="load" linkguid=\""""+main_link+"""\" />
    </PROJECT>""")
    eres = e.request(True)
    packet = e.fetch('.//EXPORTPACKET', 'guid')[0]
    
    #load references of export packet (links)
    r = RRob.RedRequestObj()
    r.setrql("""
      <PROJECT>
        <EXPORTPACKET guid=\""""+packet+"""\">
          <REFERENCES action="list" />
        </EXPORTPACKET>
      </PROJECT>""")
    rres = r.request(True)
    
    #fetch all guids from references 
    links = r.fetch(".//REFERENCE", 'guid')
    #for each link
    for link in links:
        l = RRob.RedRequestLink(link)
        lres = l.request()
        pgs = []
        # load page connected to the link
        try:
            pgs = l.fetch('.//PAGE', 'guid')
        except TypeError:#no pages connected
            continue
        if pgs is not None and len(pgs) > 0:
            for pg in pgs:
                p = RRob.RedRequestPage(pg)
                pres = p.request()
                template = ''
                try:
                    template = p.fetch('.//PAGE[@templatetitle]', 'templatetitle')[0]
                except TypeError:
                    #not a content page
                    pass
                # if page template is foundation template
                if len(template) > 0:
                    if template in red.RD_Foundation_Pages:
                        #   yield page guid
                        return_guids.append(p.fetch('.//PAGE', 'guid')[0])
    
    return return_guids
