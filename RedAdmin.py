import RedDot as red
import RedRequestObj as RRob
import RedSession

print 'redadmin imported'

sesh = RedSession.sesh

def allfollowing(guid):
    """
    Takes guid of a RedDot foundation page.
    Recursivley descends on RedDot tree.
    Returns list of all foundation page guids following input page.
    """
    childs = []
    
    def rec_allfollowing(guid):
        if guid in childs:
            print 'Warning: recursive link detected '+guid
            return

        p = RRob.RedRequestPage(guid)
        p.request()
        template = p.fetch(".//PAGE[@templatetitle]",'templatetitle')[0]
        if template in red.RD_Foundation_Pages:
            ls = p.fetch('.//LINK','guid')
            for l in ls:
                l = RRob.RedRequestLink(l)
                l.request()
                subps = l.fetch('.//PAGE','guid')
            print template#del
        else:#del
            print 'taint no foundation page!'#del

    p = RRob.RedRequestPage(guid)
    p.request()
    template = p.fetch(".//PAGE[@templatetitle]",'templatetitle')[0]
    if template in red.RD_Foundation_Pages:
            childs = childs + rec_allfollowing(guid)

    return childs
