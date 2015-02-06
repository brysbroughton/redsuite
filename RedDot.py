
#import RedAdmin, RedPressExporter
import os

"""
Namespace for handling install-specific details of RedDot API administration
auth Brys B 2015-01-06
"""

host = 'my.reddot.host:443'#must communicate through port 443
aspconnecturl = '/CMS/PlugIns/MyAspConnector.asp'
cachepath = './cache/'
RD_Error_Messages = {
    'PLEASE LOGIN': 'The user session has timed out or the Login GUID is no longer valid. Please login again.  Login.',
    '#RDERROR1': 'The number of modules in the license key does not correspond to the checksum.',
    '#RDERROR2': 'The license key is only valid for the Beta test.',
    '#RDERROR3': 'The license key is not correct. An error which could not be classified has occurred during the check.',
    '#RDERROR4': 'License is no longer valid.',
    '#RDERROR5': 'The server IP address is different than specified in the license.',
    '#RDERROR6': 'License is not yet valid.',
    '#RDERROR7': 'License is a cluster license. This error message is no longer supported beginning with CMS 6.0.',
    '#RDERROR8': 'The IP address check in the license key is not correct.',
    '#RDERROR9': 'Invalid version of the license key.',
    '#RDERROR10': 'There are duplicate modules in the license.',
    '#RDERROR11': 'A module in the license is flawed.',
    '#RDERROR12': 'There are illegal characters in the license.',
    '#RDERROR13': 'The checksum is not correct.',
    '#RDERROR14': 'The serial number in the license is not correct.',
    '#RDERROR15': 'The serial number of the license key is different from the serial number of the previous license key.',
    '#RDERROR16': 'The IP address of the Loopback adapter is not supported in this license.',
    '#RDERROR17': 'The license key contains no valid serial number.',
    '#RDERROR101': 'The user is already logged on.',
    'RDERROR110 (NoRight)': 'The user does not have the required privileges to execute the RQL. The cause of this situation may be that the logon GUID or session key has expired or the session has timed out.',
    'RDERROR201': 'Access to database "ioAdministration" has failed.',
    '#RDERROR301': 'Defective asynchronous component.',
    'RDERROR401': 'A project is locked for the executing user or the user level.',
    'RDERROR510': 'The CMS server is not available.',
    'RDERROR511': 'The CMS server or the CMS databases are updated.',
    'RDERROR707': 'The Login GUID does not correspond to the logged on user.',
    'RDERROR800': 'The maximum number of logins for a user has been reached.',
    '#RDERROR2910': 'References still point to elements of this page.',
    '#RDERROR2911': 'At least one element is still assigned as target container to a link.',
    '#RDERROR3000': 'Package already exists.',
    'RDERROR3032': 'You have tried to delete a content class on the basis of which pages have already been created.',
    'ERROR3049': 'Too many users to a license. Login to CMS failed. Please login again later.',
    'RDERROR4005': 'This user name already exists.',
    'RDERROR5001': 'The folder path could not be found or the folder does no longer exist.',
    'RDERROR6001': 'A file is already being used in the CMS.',
    'RDERROR15805': 'You have no right to delete this page.',
    'RDERROR16997': 'You cannot delete the content class. There are pages which were created on the basis of this content class in other projects.'
}
RD_Foundation_Pages = [
    #String names of all foundation page content classes - must be edited for 'all-following' feature to work
    '(Incorrect) Foundation - Online Orientation Video Feature Page',
    '(Unused) Foundation - Narrow Page (for Videos) (Unused)',
    '(Unused) SmartForms - Form Page',
    'Annual Report - Wide Image Page',
    'Bookstore - Foundation - Homepage',
    'Bookstore - Foundation - Wide Image Page',
    'Chancellors Leadership Academy - Foundation - Homepage',
    'CWD - Foundation - Homepage',
    'CWD - Foundation - Wide Image Page',
    'File Library Page',
    'Fine Arts - Foundation - Homepage',
    'Fine Arts - Foundation - Single Fine Arts Page',
    'Foundation - Booklist - Single Course List',
    'Foundation - Campuses/Locations - Main Layout',
    'Foundation - Campuses/Locations - Single Location Layout (unused)',
    'Foundation - Cashier - Left Navigation Page',
    'Foundation - Cashier Services Homepage',
    'Foundation - Catalog - Single Course Layout',
    'Foundation - Catalog Program Layout',
    'Foundation - Department Video Feature Page',
    'Foundation - Directory - A-Z Index Page',
    'Foundation - Directory - Department Directory Page',
    'Foundation - Directory - Employee Directory Page',
    'Foundation - Financial Aid - Single Notification',
    'Foundation - Financial Aid - Student Notifications List',
    'Foundation - Full-Width Page',
    'Foundation - Job Vacancy Layout',
    'Foundation - Left Image Page',
    'Foundation - Online Orientation Video Feature Page',
    'Foundation - Right Image Page',
    'Foundation - Self Study - Full Image Page',
    'Foundation - Self Study - Resource Room Page',
    'Foundation - Single Article',
    'Foundation - Single FAQ Page', #treat as body content for export
    'Foundation - Single Press Release',
    'Foundation - Static Full-Width Page',
    'Foundation - Strategic Planning - Full Image Page',
    'Foundation - Video Feature Page',
    'Foundation - Video Feature Page (External Host)',
    'Foundation - Wide Image Page',
    'Foundation - Work Study Vacancy Layout',
    'Homepage',
    'Locations - Foundation',
    'OTC Foundation - Foundation - Homepage',
    'OTC Foundation - Foundation - Wide Image Page',
    'OTC Online - Foundation - Homepage',
    'OTC Online - Foundation - Wide Image Page',
    'OTC Profiles - Foundation - Single Profile Page',
    'Policies And Procedures - Foundation - Wide Image Page',
    'Print Shop - Foundation - Homepage',
    'Print Shop - Foundation - Wide Image Page',
    'Testing  DO NOT USE!!!',
    'Testing - Foundation - Wide Image Page (Do Not Use)',
    'Tutoring - Foundation - Homepage',
    'Start Page',
    'Mobile Content Page',
    'Mobile Homepage',
    'Foundation - Form page'
    ]

def parse_date(datestr):
    """
    Accepts date string formatted like YYYY-MM-DD
    Returns corresponding RedDot ordinal date as numerical string
    """
    reg = re.compile('^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
    if reg.match(datestr):
        datear = datestr.split('-')
        datear = map(lambda x: int(x, 10), datear)
        try:
            import datetime
            datein = datetime.datetime(datear[0], datear[1], datear[2])
            redordinal = datein.toordinal() - 693594 #The Red epoch is 693594 days before the python epoch
            return str(redordinal)
        except Exception as ex:
            print "Error evaluating date. Please ensure a valid date was entered."
            return ''
    else:
        print "Expected date string of format YYYY-MM-DD at: " + str(datestr)
        return ''
    
def wp_date(ordinal):
    """
    Accepts float or string float representing RedDot ordinal Date.
    Returns WordPress type date in GMT. ex:
    2014-12-02 00:00:00
    """
    import datetime
    
    rdtime = '0'
    try:
        rdtime = ordinal.split('.')[1] #the decimal portion represents the time of day
    except Exception as ex:
        #no decimal means no time of day in ordinal
        raise
    #time
    timesum = 0
    magnitude = 0
    for digit in rdtime:
        timesum = timesum + int(digit) * 8640*10**magnitude # RedDot time conversion is undocumented. But, this heuristic works and is tested.
        magnitude -= 1
    timesum = int(round(timesum))
    time_string = str(datetime.timedelta(seconds=timesum))

    #date
    ordinal = float(ordinal)
    rddate = int(ordinal)
    pyordinal = rddate + 693594 #The Red epoch is 693594 days before the python epoch
    
    #format string
    return_string = datetime.date.fromordinal(pyordinal).isoformat()#yyyy-mm-dd
    return_string = return_string+' '+time_string
    return return_string
    
def cache(guid, res):
    """
    Takes a guid and its RedDot Response and caches in the local cache directory
    No return value
    """
    #todo - temporarily disabling cache
    #return
    if not os.path.exists(cachepath):
        os.mkdir(cachepath)
    
    f = open(cachepath+guid+'.xml', 'w')
    f.write(res)
    f.close()


def cached(guid):
    """
    Takes guid and checks if its information is stored in the local cache
    Returns boolean
    """
    #todo - temporarily disabling cache
    #return False
    return os.path.exists(cachepath+'/'+guid+'.xml')
    

def getcached(guid):
    """
    Takes guid and returns locally cached RedDot response for that guid
    """
    #todo
    #make cache enable/disable functions
    #raise Exception("File not in local cache")#temporarily 'disabling cache'

    if cached(guid):
        print 'loading cached response '+cachepath+guid+'.xml'
        f = open(cachepath+guid+'.xml', 'r')
        res = f.read()
        f.close()
        return res
    else:
        raise Exception("File not in local cache")
    
    