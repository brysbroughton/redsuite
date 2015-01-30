import RedDot as red
import RedRequestObj as RRob
import RedPressExporter as rp
import RedSession
import xml.etree.ElementTree as ET
import pprint as pp
print 'redadmin imported'

sesh = RedSession.sesh

def allfollowing(guid, func_in=None):
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
            if func_in is not None:
                func_in(p)
            
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


def allinpub(guid, func_in=None):
    """
    Takes guid of a foundation page.
    Returns set of all guids of foundation pages with the same publication package.

    <IODATA loginguid="[!guid_login!]" sessionkey="[!key!]">
      <PROJECT>
        <EXPORTPACKET guid="[!guid_exportpacket!]">
          <REFERENCES action="list" />
        </EXPORTPACKET>
      </PROJECT>
    </IODATA>
        
    """
    return_guids = set([])
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
        linktype = l.fetch('.//LINK','islink')[0]
        if linktype != '1' and linktype != '2':
            #skip empty links and references
            continue
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
                    if func_in is not None:
                        func_in(p)#passing to logtemplatecount
                    if template in red.RD_Foundation_Pages:
                        #   yield page guid
                        return_guids.add(p.fetch('.//PAGE', 'guid')[0])
    
    return return_guids


def subsite(guid, func_in=None):
    """
    Takes guid of root foundation page.
    Recurses down tree as 'allfollowing'.
    Does not follow branches with different publication packages.
    Returns list of all foundation page guids, excluding the root page guid.
    """
    childs = set([])
    visited_guids = set([])
    pub_set = allinpub(guid)#set of foundation page guids 

    rec_log = open('recursive_links.txt','w')
    
    def rec_allfollowing(guid):
        print "evaluating page "+guid
        if guid in visited_guids:
            print 'Warning: recursive link detected '+guid
            rec_log.write(guid+"\n")
            return
        visited_guids.add(guid)

        p = RRob.RedRequestPage(guid)
        p.request()
        try:
            template = p.fetch(".//PAGE[@templatetitle]",'templatetitle')[0]
        except TypeError:
            #Occurs when no templatetitle = not a content page
            return
            pass
        if template in red.RD_Foundation_Pages:
            if guid in pub_set:
                childs.add(guid)
                if func_in is not None:
                    func_in(p)
            else:#pub package check - not part of subsite
                return
            
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
    sh = p.request()
    template = p.fetch(".//PAGE[@templatetitle]",'templatetitle')[0]
    if template in red.RD_Foundation_Pages:
            rec_allfollowing(guid)
    else:
        raise Exception('Requires guid of root foundation page')
        
    try:
        childs.remove(guid)#don't return input guid as a child of itself
    except KeyError:
        #it wasn't in the set anyway
        pass
    rec_log.close()
    return childs


counts = {}

def logtemplatecount(reqo):
    """
    Takes a request object as input.
    Writes to file, keepoing count of content class.
    Pass to other function for automation tasks.
    """
    if reqo.getrql() is None or len(reqo.getrql()) == 0:
        raise Exception('Request object not ready')
    
    if reqo.redResponse is None or len(reqo.redResponse) == 0:
        reqo.request(True)

    print 'logtemplate '+reqo.fetch('.//PAGE[@templatetitle]', 'templatetitle')[0]
    print reqo.fetch('.//PAGE[@id]', 'id')[0]

    template = reqo.fetch('.//PAGE[@templatetitle]', 'templatetitle')[0]
    if counts.has_key(template):
        counts[template] = counts[template] + 1
    else:
        counts[template] = 1

pubs = {}


def getpubname(guid):
    """
    Takes guid of page.
    Determines name of publication package.
    stores in pub dictionary.
    """
    pass


def logpubcount(reqo):
    """
    Takes a request object as input.
    Counts occurrences of pub package attached
    """
    #get mainlink guid
    main_link = reqo.fetch(".//LINK[@ismainlink='1']", 'guid')[0]
    
    #load exportpacket of mainlink guid
    e = RRob.RedRequestObj()
    e.setrql("""  <PROJECT>
    <EXPORTPACKET action="load" linkguid=\""""+main_link+"""\" />
    </PROJECT>""")
    eres = e.request(True)
    pubname = e.fetch('.//EXPORTPACKET', 'name')[0]

    if pubs.has_key(pubname):
        pubs[pubname] = pubs[pubname] + 1
    else:
        pubs[pubname] = 1


log = open('log.txt', 'w')

def writelog(reqo):
    """
    Take page request object and file writer
    Write information to file
    Pass to other function for automation
    """
    if reqo.getrql() is None or len(reqo.getrql()) == 0:
        raise Exception('Request object not ready')
    
    if reqo.redResponse is None or len(reqo.redResponse) == 0:
        reqo.request(True)

    template = ''
    try:
        template = reqo.fetch('.//PAGE[@templatetitle]', 'templatetitle')[0]
    except TypeError:
        template = 'NO TEMPLATE FOUND'

    pageid = reqo.fetch('.//PAGE[@id]','id')[0]
    headline = reqo.fetch('.//PAGE[@headline]', 'headline')[0]
    guid = reqo.fetch('.//PAGE', 'guid')[0]

    out = guid+' '+pageid+' '+headline+' '+template
    try:
        out = out.decode('latin-1').encode('utf-8')#handling unicode characters
    except UnicodeEncodeError:
        out = guid+' '+pageid+' UNICODE ERROR '+template
        
    log.write(out)
    

    
