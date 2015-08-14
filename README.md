# redsuite
<h1>Python automation library for RedDot CMS 7.5</h1>
<h2>Overview</h2>
<p>The RedDot Content Management System provides a vastly configurable, albeit closed-source, solution for enterprise level websites. The GUI allows for limited editing on the part of the end-users, and a few utilities for automation for the administrators. However, the utilities fall short of many of the automation needs necessary to meet the complexity of the system. There is no way provided to, say, push all pages of a sub-site through the workflow, or delete said pages. There's also a large lack of analytic tools; in case you want to count something like the number of map widgets created this year, you will basically have no way to attain that knowledge. Even estimating the number of total Web pages in your project is impossible with the default tools. This framework aims to provide a means to acquire these assets, and be extended to acquire others as needed.</p>
<h2>Structure</h2>
<p>The RedDot system runs on classic ASP pages with VBScript. Using ASP, devs may extend the functionality of the system through plugins written in ASP, essentially creating interactive ASP webpages. But rather than going to the trouble of creating a whole interactive Web forms system, or full-fledge Web services, many devs in recent years opt for a simple ASP connector file (RedPlug.asp) that receives POST requests containing the XML query payload, passes the XML in to a RedDot server object to be evaluated, and returns the XML from the server object back in the POST request.</p>
<p>Python script -> POST request with XML query -> RedPlug.asp -> RedDot runtime evaluates XML -> Result XML returned to Python</p>
<p>This XML that is exchanged between the script and the RedDot runtime is a proprietary RQL format (Resource Query Language). Some <a href="http://www.reddotcmsblog.com/rql-in-a-nutshell-part-1" target="_blank">great blogs</a> have been written about using this format. If you are going to implement a similar project at your organization, you'll need to find the official RQL documentation for your version of RedDot/OpenText CMS.</p>
