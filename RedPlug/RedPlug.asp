<%
'set reponse encoding
Response.ContentType = "text/html"
Response.AddHeader "Content-Type", "text/html;charset=UTF-8"
Response.CodePage = 65001
Response.CharSet = "UTF-8"

'create the reddot server objects
Dim objIO
Dim RQL, sError, RQL_Request

set RQLObject = Server.CreateObject("RDCMSAsp.RdPageData")
RQLObject.XmlServerClassName = "RDCMSServer.XmlServer"
'const DhtmlClassName = "RDCMSAsp.RdPageData"

RQL = Request.Form("RQL")
RQL_Request = RQLObject.ServerExecuteXml(RQL, sError)
if sError > "" then
	response.write "<ERROR>" + sError + "</ERROR>"
else
	response.write RQL_Request
end if

%>