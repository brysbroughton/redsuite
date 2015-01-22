from __future__ import print_function
print('redpressexporter imported')

import RedDot as red
import RedRequestObj as RRob
import RD2WXR_Definitions as wxr
import RedSession
import RedAdmin
import datetime, time, re
import pprint

sesh = RedSession.sesh

class RedPress(object):

    f = None
    assetpath = '/'
    wp_subsite_path = None#to be set in cases of mass exporting

    def __init__(self):
        new_path = "Enter new path for exported assets? (y/n)"
        if new_path.upper() == 'Y':
            new_path_in = raw_input("New path with beginning and ending slashes: ")
            self.setassetpath(new_path_in)
            
    def setsubsitepath(self, path):
        self.wp_subsite_path = path
        
    def getsubsitepath(self):
        return self.wp_subsite_path

    def call_export_func(self, rro, tup):
        """
        Takes tuple of (funcname, arg) and a red request object
        Calls appropriate export function
        """
        #pprint.pprint(tup)
        fun = tup[0]
        val = tup[1]
        if fun == 'placeholder':
            print('placeholder: '+val)
            if val == 'wp_filename':
                self.f.write(wxr.wp_fileurl(rro.fetch('.//PAGE[@headline]', 'headline')[0]))
            else:
                #case 0: placeholder is in PAGE tag
                #   just print here
                try:
                    pval = rro.fetch('.//PAGE[@'+ val+']', val)[0]
                    self.f.write(pval)
                    print(pval)
                    return
                except Exception as ex:
                    pass#placeholder is not in PAGE tag
                #case 1: placeholder is in ELEMENT tag
                #   call export element
                guid = rro.fetch(".//*[@name='"+val+"']", 'guid')[0]
                self.exportelement(guid)
        elif fun == 'IoRangeContainer':
            self.exportcontainer(rro.fetch(".//LINK[@name='"+val+"']", 'guid')[0])
        elif fun == 'IoRangeListContent':
            self.exportcontainer(rro.fetch(".//LINK[@name='"+val+"']", 'guid')[0])
        elif fun == 'IoRangeListLink':
            ast = wxr.parse(val)
            #ast= [text, placeholder, text]
            #example: <%lst_list2%>Links - Large Bulleted Link List - wxr item<%/lst_list2%>
            con_name = ast[1][0]
            guid = rro.fetch(".//LINK[@eltname='"+con_name+"']", 'guid')[0]
            specialwxr = ast[1][1]
            self.exportlist(guid, specialwxr)
        elif fun == 'IoRangeConditional':
            ast = wxr.parse(val)
            placeholder = ast[1][1]
            pval = rro.fetch(".//ELEMENT[@name='"+placeholder+"']", 'value')[0]
            if pval:
                pguid = rro.fetch(".//ELEMENT[@name='"+placeholder+"']", 'guid')[0]
                self.f.write(ast[0])
                self.exportelement(pguid)
                self.f.write(ast[2])
        else:
            raise Exception("No function defined for placeholder " + fun)

    def export(self, ps):
        """
        Accepts mixed list of page descriptions
        Each description is one of the following:
            1. String guid of foundation page (non-foundation pages will be ignored)
            2. Tuple of strings ([guid_page], [wordpressID_parent], [wordpressTitle_parent]) - for child pages
        """
        if type(ps).__name__ != 'list':
            raise Exception('export accepts a mixed list. check docstring with dir.')
        
        print("Starting export job")
        self.f = open('RedPressWXRExport'+str(time.time())+'.xml','w')
        self.f.write(wxr.header)
        pprint.pprint(ps)
        for p in ps:
            if type(p).__name__ == 'str':
                self.exportfoundation(p)
            elif type(p).__name__ == 'tuple':#todo - unused
                self.exportsubfoundation(p[0], p[1], p[2]) 
            else:
                print('unexpected page input: ' + p)
        self.f.write(wxr.footer)
        self.f.close()

    def exportsite(self):
        """
        Takes input from user describing root page of site
            (reddot_guid, wordpress_id, wordpress_title)
        *Root page must have already been imported to Wordpress
        """
        print("Root page must already be imported to Wordpress")
        rootguid = raw_input("Enter guid of root page: ")
        wpid = raw_input("Enter Wordpress id of root page: ")
        wptitle = raw_input("Enter exact title of root page in Wordpress: ")
        
        self.setsubsitepath(wptitle)
        self.f = open('RedPressWXRExport'+str(time.time())+'.xml','w')
        self.f.write(wxr.header)
        self.f.write("""
	<item>
		<title>"""+wptitle+"""</title>
		<wp:post_id>"""+wpid+"""</wp:post_id>
		<wp:post_type>page</wp:post_type>
	</item>""")
        
        childs = RedAdmin.allfollowing(rootguid)
        for c in childs:
            self.exportsubfoundation(c, wpid)
            
        self.f.write(wxr.footer)
        self.f.close()
        
    def exportfoundation(self, guid):
        o = RRob.RedRequestPage(guid)
        o.request()
        #verify is foundation page
        if o.fetch('.//PAGE[@templatetitle]', 'templatetitle', 1)[0] not in red.RD_Foundation_Pages:
            print('Warning: '+guid+' is not a foundation page. Nothing exported.')
            return

        ast = wxr.parse(wxr.wpds['Generic Foundation']['html'])
        #pprint.pprint(ast)
        for t in ast:
            typ = type(t).__name__
            if typ == 'str':
                self.f.write(t)
            elif typ == 'tuple':
                self.call_export_func(o, t)
            else:
                raise Exception("Incorrect type in ast at " + t)
       

    def exportsubfoundation(self, guid, parent_id):
        """
        Exporting a subpage requires the parent page is already imported.
        Must supply exact id of page in wordpress.
        """
        o = RRob.RedRequestPage(guid)
        o.request()
        #verify is foundation page
        if o.fetch('.//PAGE[@templatetitle]', 'templatetitle', 1)[0] not in red.RD_Foundation_Pages:
            print('Warning: '+guid+' is not a foundation page. Nothing exported.')
            return
        
        ast = wxr.parse(wxr.wpds['Generic Sub Foundation']['html'])
        for t in ast:
            typ = type(t).__name__
            if typ == 'str':
                self.f.write(t)
                #print(t)
            elif typ == 'tuple':
                if t == ('placeholder', 'wp_parentid'):
                    self.f.write(parent_id)
                    #print(parent_id)
                else:
                    self.call_export_func(o, t)
            else:
                raise Exception("Incorrect type in ast at " + t)


    def exportpage(self, guid, wxr_def=None):
        """
        Generic page export for content pages
        """
        o = RRob.RedRequestPage(guid)
        o.request()
        #get template name
        if wxr_def is None:
            wxr_def = o.fetch('.//PAGE[@templatetitle]', 'templatetitle')[0]
        print('export page of type: '+wxr_def)#debug
        ast = wxr.parse(wxr.wpds[wxr_def]['html'])
        #pprint.pprint(ast)
        for t in ast:
            typ = type(t).__name__
            if typ == 'str':
                self.f.write(t)
            elif typ == 'tuple':
                self.call_export_func(o, t)
            else:
                raise Exception("Incorrect type in ast at " + t)


    def exportcontainer(self, guid):
        """
        Takes file writer object, guid of structural link
        Exports all pages connected to the structural link
        islink:
        0 = No structural element
        1 = Simple structural element
        2 = Multilink (z. B. List or Container)
        10  = Reference to a structural element 
        """
        #print('exportcontainer: '+guid)
        o = RRob.RedRequestLink(guid)
        o.request()
        #check link type in case of refernce to other containers
        islink = o.fetch('.//LINK', 'islink')[0]
        print('linktype: '+islink)
        # 0 = not a link
        if islink == '0':
            raise Exception('Export link called on non-link element: '+guid)
        # 1 = anchor, 2 = multilink
        elif islink == '1' or islink == '2':
            if islink == '1':
                print('WARNING: exportcontainer called on simple anchor '+guid)
            pgs = o.fetch('.//PAGE', 'guid')
            if pgs:
                for pg in pgs:
                    self.exportpage(pg)
            else:
                print('Empty container: '+guid)
        #10 = reference to other element
        elif islink == '10':
            r = RRob.RedRequestReference(guid)
            r.request(True)#True = don't cache tree segment
            ref_guid = r.fetch('.//TREESEGMENTS/SEGMENT[last()]', 'guid')
            ref_typ = r.fetch('.//TREESEGMENTS/SEGMENT[last()]', 'type')
            if ref_type == 'link':
                self.exportcontainer(ref_guid)
            elif ref_type == 'page':
                self.exportpage(ref_guid)
            else:
                print('Error: Illegal reference detected: '+guid)
        else:
            raise Exception('Unrecognized link type: '+islink+' at '+guid)

    def exportlist(self, guid, wxr_def):
        """
        Takes file writer object, guid of structural link, name of wxr definition
        Exports all pages connected to the structural link, according to the definition
        islink:
        0 = No structural element
        1 = Simple structural element
        2 = Multilink (z. B. List or Container)
        10  = Reference to a structural element 
        """
        #print('exportlist: '+guid)
        #print('wxr_def: '+wxr_def)
        o = RRob.RedRequestLink(guid)
        o.request()
        #check link type in case of reference to other containers
        islink = o.fetch('.//LINK', 'islink')[0]
        #0 = not a link
        if islink == '0':
            raise Exception('Exportlink called on non-link element: '+guid)
        #1 = anchor, 2 = multilink
        elif islink == '1' or islink == '2':
            if islink == '1':
                print('WARNING: exportlist called on simple anchor '+guid)
            pgs = o.fetch('.//PAGE', 'guid')
            if pgs:
                for pg in pgs:
                    self.exportlistitem(pg, wxr_def)
            else:
                print('Empty list: '+guid)
        #10 = reference to other link or page
        elif islink == '10':
            r = RRob.RedRequestReference(guid)
            r.request(True)#True = don't cache tree segment
            ref_guid = ''
            ref_type = ''
            try:
                ref_guid = r.fetch('.//TREESEGMENTS/SEGMENT[last()]', 'guid')[0]
                ref_type = r.fetch('.//TREESEGMENTS/SEGMENT[last()]', 'type')[0]
            except Exception as ex:
                #A reference with no tree segments is the un-recoverable assign url on anchor
                self.f.write('[assigned url on link guid'+guid+']')
                return
                pass
            if ref_type == 'link':
                self.exportlist(ref_guid, wxr_def)
            elif ref_type == 'page':
                self.exportlistitem(ref_guid, wxr_def)
            else:
                print('Error: Illegal reference detected: '+guid)
        else:
            raise Exception('Unrecognized link type: '+islink+' at '+guid)


    def exportlistitem(self, item_guid, wxr_def):
        """
        May take guid of special Assign url page or regular page and
        a wxr definition name
        exports to file object
        """
        o = RRob.RedRequestObj(item_guid)
        o.setrql('<LINK action="load" guid="'+item_guid+'"><URL action="load" /></LINK><PAGE action="load" guid="'+item_guid+'" />')
        o.request(True)#True = don't cache these bc not sure which request type is correct
        src=''
        try:
            src = o.fetch('.//URL', 'src')[0]
        except Exception as ex:
            #there is no src implies this is a regular page
            pass

        if not src:
            #get page link values
            src = self.getlinktopage(item_guid)
        if not src:
            #output nothing if src can't be determined
            return

        ast = wxr.parse(wxr.wpds[wxr_def]['html'])
        for t in ast:
            typ = type(t).__name__
            if typ == 'str':
                self.f.write(t)
            elif typ == 'tuple':
                if t[0] != 'placeholder':
                    raise Exception('Parse Error in exportlistitem: only simple placeholders allowed in '+wxr_def)
                if t[1] == 'URL':#URL is special RedPress wxr placeholder, not in RedDot
                    self.f.write(src)
                else:
                    val = o.fetch('.//PAGE', t[1])[0]
                    if not val:
                        print("Warning: "+t[1]+" value not found on page "+item_guid)
                    else:
                        self.f.write(val)
            else:
                raise Exception('Parse Error in exportlistitem: '+wxr_def)


    def exportelement(self, guid):
        """
        Takes element guid and gets value to export
        Writes to file pointer
        """
        o = RRob.RedRequestElement(guid)
        o.request()#True)#True = don't cache 
        #if refelementguid exists for element, must load this guid in place of element
        try:
            refguid = o.fetch(".//ELT']", 'refelementguid')[0]
            self.exportelement(refguid)
            return
        except Exception as ex:
            pass

        typ = o.fetch('.//ELT', 'elttype')[0]
        val = o.fetch('.//ELT', 'value')[0]

        print('element: '+guid)
        print('element type: '+typ)
        print('element value: '+val)

        if len(val) == 0:
            return #todo - is this safe for all element types?

        #standard field
        if typ in set(['1','5','39','48','999','50','51','1000']):
            self.f.write(val)
        #text
        elif typ in set(['31','32']):
            self.exporttext(guid)
        #image
        elif typ == '2':
            #later can maybe extend to use properties of elements and get 
            subdirguid = o.fetch('.//ELT', 'subdirguid')[0]
            out = self.getassetpath(subdirguid)+val
            print('image out: '+out)
            self.f.write(self.getassetpath(subdirguid)+val)
        #option list
        elif typ == '8':
            #if value=''
            #try eltdefaultselectionguid=''
            selected_guid = o.fetch('.//ELT', 'value')[0]
            if selected_guid:
                val = o.fetch(".//SELECTION[@guid='"+selected_guid+"']", 'value')[0]
                self.f.write(val)
            else:
                default_guid = o.fetch('.//ELT', 'eltdefaultselectionguid')[0]
                if default_guid:
                    val = o.fetch(".//SELECTION[@guid='"+default_guid+"']", 'value')[0]
                    self.f.write(val)
        #media
        elif typ == '38':
            #later can maybe extend to use properties of elements and get attributes
            subdirguid = o.fetch('.//ELT', 'subdirguid')[0]
            print('image out: '+self.getassetpath(subdirguid)+val)
            self.f.write(self.getassetpath(subdirguid)+val)
        else:
            print('warning: unhandled elem type exported: '+typ+' '+guid)
            self.f.write('[element guid:'+guid+']')


    def exporttext(self, guid):
        """
        Requests text blob and evaluates any [ioID]guid's before writing out
        """
        t = RRob.RedRequestText(guid)
        text = t.request(True)
        ioIDs = re.findall('\[ioID\][A-F0-9]{32}/?', text)
        for ioID in ioIDs:
            ioguid = ioID.replace('[ioID]', '').replace('/','')
            f = RRob.RedRequestFolder(ioguid)
            fres = f.request(True)
            if(f.err()):
                #self.f.write(self.getlinktopage(ioguid))
                text = text.replace(ioID, self.getlinktopage(ioguid))
            else:
                #self.f.write(self.getassetpath(ioguid))
                text = text.replace(ioID, self.getassetpath(ioguid))
        self.f.write(text)
        

    def getassetpath(self, guid):
        """
        Returns arbitrarily defined path for exported assets
        """
        return self.assetpath


    def setassetpath(self, path):
        self.assetpath = path


    def getfolderpath(self, guid):
        """
        Takes folder guid, requests.
        Returns folder path
        """
        f = RRob.RedRequestFolder(guid)
        f.request()
        path = f.fetch('.//FOLDER', 'path')[0]
        pprint.pprint(path)
        path = path.replace('\\', '')
        #todo - change host to new system host
        return '//www.otc.edu/'+path+'/'


    def getlinktopage(self, guid):
        """
        Returns link to foundation page or
        None if input guid is not a foundation page
        """
        p = RRob.RedRequestPage(guid)
        p.request()
        path = p.fetch(".//PROJECTVARIANT[@name='HTML']//EXPORTFOLDER[@foldername='Published pages']", 'folderpath')[0]
        if self.getsubsitepath() is not None:
            path = self.getsubsitepath()
        fname = wxr.wp_fileurl(p.fetch(".//PAGE[@headline]", 'headline')[0])
        return '/' + path+'/'+fname


rp = RedPress()
