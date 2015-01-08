print 'RedSession imported'

import RedDot as red
import RedRequestObj
import pprint

RRob = RedRequestObj.RedRequestObj

class RedSession(object):

    sessionkey = ''
    loginguid = ''
    user = ''
    password = ''

    def setsessionkey(self, key):
        self.sessionkey = RedRequestObj.sessionkey = key

    def setloginguid(self, guid):
        self.loginguid = RedRequestObj.loginguid = guid

    def __init__(self, sessionkey='', loginguid=''):
        self.sessionkey = RedRequestObj.sessionkey = sessionkey
        self.loginguid = RedRequestObj.loginguid = loginguid

    def login(self):
        self.user = raw_input('Username: ')
        self.password = raw_input('Password: ')
        o = RRob()
        o.setrql('<IODATA><ADMINISTRATION action="login" name="' + self.user + '" password="' + self.password + '" /></IODATA>', True)
        print o.request()

        loginguid = o.fetch('./LOGIN', 'guid', 1)[0]
        if loginguid is not None:
            if len(loginguid) > 0:
                self.setloginguid(loginguid)
                print self.loginguid
                #create dictionary of project guids
                pnodes = o.getXpath(o.redResponse, './USER/LASTMODULES//MODULE')
                pdict = {node.attrib['projectname'].upper() : node.attrib['project'] for node in pnodes}
                self.loginProjectSelect(pdict)
            else:
                print 'Incorrect username'
        else:
            print o.err()

    def loginProjectSelect (self, pdict):
        """
        Should be called by red.login, expects pdict to be dictionary
        from login response of form {project_name:project_guid}
        **Can only display projects that user has logged in to before
        """
        print "Enter a project name, or 'C' to cancel\n"
        for p in pdict: print p
        user_in = raw_input().upper()
        if user_in == 'C':
            return
        elif pdict.has_key(user_in):
            o = RRob()
            o.setrql('<IODATA loginguid="'+self.loginguid+'">' + '<ADMINISTRATION action="validate" guid="'+self.loginguid+'" useragent="script"><PROJECT guid="'+pdict[user_in]+'" /></ADMINISTRATION></IODATA>', True)
            res = o.request()
            self.setsessionkey(o.fetch('.//SERVER', 'key', 1)[0])
        else:
            print "\n***invalid project name***\n"
            self.loginProjectSelect(pdict)
        
        
    def logout(self, user_in=None):
        o = RRob()
        o.setrql('<IODATA loginguid="' + self.loginguid + '" ><ADMINISTRATION><LOGOUT guid="' + self.loginguid +  '" /></ADMINISTRATION></IODATA>', True)
        return o.request()


sesh = RedSession()
