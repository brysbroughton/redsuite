#Handles WXR template generating with RedDot page elements
#To be imported for use in the RedLine Exporting function
#Auth Brys B 2014-12
#
#denote RedDot Elements by placeholders e.g. <%hdl_headline/%>
##placeholders cannot have whitespace
#
##simple place holders have trailing slashe.g. <%hdl_headline/%>
#
##placeholders for containers and lists have opening and closing tags
##e.g. <%IoRangeConditional%><%stf_description/%><%/IoRangeConditional%>
#
##Lists and containers must be nested e.g.
##<%IoRangeListLink%><%lst_listitems%><li><%hdl_headline/%></li><%/lst_listitems%><%/IoRangeListLink%>
#
##Supported Containers: IoRangeConditional, IoRangeListLink, IoRangeListContent
#
##IoRangeConditional can nest only one placeholder as argument
#
import datetime

wordpresshost = 'http://philip.ozarkstech.org'

def wp_fileurl(headline):
    """
    Takes string page headline
    Converts to wp-friendly url string and returns
    """
    reg = re.compile('[^0-9a-zA-Z]+')
    tokens = [x for x in re.split(reg, headline) if x not in ['', ' ']]
    return '-'.join(tokens)

header = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
	xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
	xmlns:content="http://purl.org/rss/1.0/modules/content/"
	xmlns:wfw="http://wellformedweb.org/CommentAPI/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
	<title>Ozarks Technical Community College</title>
	<link>http://philip.ozarkstech.org</link>
	<description></description>
	<pubDate>Wed, 03 Dec 2014 20:52:45 +0000</pubDate>
	<language>en-US</language>
	<wp:wxr_version>1.2</wp:wxr_version>
	<wp:base_site_url>"""+wordpresshost+"""</wp:base_site_url>
	<wp:base_blog_url>"""+wordpresshost+"""</wp:base_blog_url>
	<wp:author><wp:author_id>2</wp:author_id>
        <wp:author_login>brys</wp:author_login>
        <wp:author_email>broughtb@otc.edu</wp:author_email>
        <wp:author_display_name><![CDATA[Brys Broughton]]></wp:author_display_name>
        <wp:author_first_name><![CDATA[Brys]]></wp:author_first_name><wp:author_last_name><![CDATA[Broughton]]></wp:author_last_name></wp:author>
	<generator>RedSuite v2.0</generator>"""

footer = """</channel>
</rss>"""

wpds = {
    'Text - H3 (Main) Heading and Paragraph':
    {
        'html':"""<h3><%hdl_headline/%></h3>\n<div><%txt_text/%></div>"""
        
    },
    
    'Links - Large Bulleted Link List (Two Columns)':
    {
        'html':"""
            <h4><%hdl_headline/%></h4>
            <%IoRangeConditional%><p><%txt_list_desc/%></p><%/IoRangeConditional%>
            <div class="two-column_links wrapper">
                <ul class="big_links two-column_links_1 wrapper">
                    <%IoRangeListLink%><%lst_list1%>Links - Large Bulleted Link List - wxr item<%/lst_list1%><%/IoRangeListLink%>
                </ul>
                <ul class="big_links two-column_links_2 wrapper">
                    <%IoRangeListLink%><%lst_list2%>Links - Large Bulleted Link List - wxr item<%/lst_list2%><%/IoRangeListLink%>
                </ul>
            </div>"""
    },
    
    'Links - Large Bulleted Link List - wxr item':
    {
        'html':"""<li><a href="<%URL/%>"><span class="big_links_span"><%hdl_headline/%></span></a></li>\n"""
    },
    
    'Links - Small Bulleted Link List (Two Columns)':
    {
        'html':"""
            <h4><%hdl_headline/%></h4>
            <%IoRangeConditional%><p><%txt_list_desc/%></p><%/IoRangeConditional%>
            <div class="two-column_links wrapper">
                <ul class="feature_links two-column_links_1 wrapper">
                    <%IoRangeListLink%><%lst_list1%>Links - Small Bulleted Link List - wxr item<%/lst_list1%><%/IoRangeListLink%>
                </ul>
                <ul class="feature_links two-column_links_2 wrapper">
                    <%IoRangeListLink%><%lst_list2%>Links - Small Bulleted Link List - wxr item<%/lst_list2%><%/IoRangeListLink%>
                </ul>
            </div>"""
    },
    
    'Links - Small Bulleted Link List - wxr item':#Repeating link snippet from link list
    {
        'html':"""<li><a href="<%URL/%>"><span class="feature_links_span"><%hdl_headline/%></span></a></li>\n"""
    },
    
    'Bio Box (Large)':
    {
        'html':"""
            <div class="content_bio_box_large wrapper">
                <img src="<%img_bioImage/%>" border="0" alt="<%hdl_headline/%>" class="content_bio_image" />
                <div class="content_bio_info wrapper">
                    <a href="mailto:<%stf_email/%>" class="mail_icon" title="Email <%hdl_headline/%>"><span>Email <%hdl_headline/%></span></a>
                    <h3><%hdl_headline/%></h3>
                    <%IoRangeConditional%><h4><%stf_positionTitle/%></h4><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree1/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree2/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree3/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree4/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree5/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditionalAnchor%><%anc_website%>Bio Box (Large) - wxr item - website link<%/anc_website%><%/IoRangeConditionalAnchor%>
                    <%IoRangeConditional%><h5 class="highlight-blue">Office: <%stf_officeNumber/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5 class="highlight-blue">Phone: <%stf_phoneNumber/%></h5><%/IoRangeConditional%>
                </div>
                <%IoRangeConditional%><p><%txt_text/%></p><%/IoRangeConditional%>
            </div>"""
    },
    
    'Bio Box (Large) - wxr item - bio image':
    {
        'html':"""<img src="<%img_bioImage/%>" border="0" alt="<%hdl_headline/%>" class="content_bio_image" />"""
    },
    
    'Bio Box (Large) - wxr item - website link':
    {
        'html':"""<h5><a href="<%anc_website/%>" title="<%stf_websiteTitle/%>" target="_blank" class="bio_link"><%stf_websiteTitle/%></a></h5>"""
    },
    
    'Bio Box (Small)':
    {
        'html':"""                <div class="content_bio_box wrapper">
                <img src="<%img_bioImage/%>" border="0" alt="<%hdl_headline/%>" class="content_bio_image" />
                <div class="content_bio_info boxes wrapper">
                    <a href="mailto:<%stf_email/%>" class="mail_icon" title="Email <%hdl_headline/%>"><span>Email <%hdl_headline/%></span></a>
                    <h3><%hdl_headline/%></h3>
                    <h4><%stf_positionTitle/%></h4>
                    <%IoRangeConditional%><h5><%stf_degree1/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree2/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree3/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree4/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree5/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditionalAnchor%><%anc_website%>Bio Box (Small) - wxr item - website link<%/anc_website%><%/IoRangeConditionalAnchor%>
                    <h4 class="highlight-blue">
                        <%IoRangeConditional%>Office: <%stf_officeNumber%><%/IoRangeConditional%>
                        <%IoRangeConditional%>Phone: <%stf_phoneNumber%><%/IoRangeConditional%>
                    </h4>
                </div>                            
                <%IoRangeConditional%><p><%txt_text%></p><%/IoRangeConditional%>
            </div>"""
    },
    
    'Bio Box (Small) - wxr item - website link':
    {
        'html':"""<h5><a href="<%anc_website/%>" title="<%stf_websiteTitle/%>" target="_blank" class="bio_link"><%stf_websiteTitle/%></a></h5>"""
    },
    
    'Catalog - Program Overview':
    {
        'html':"""
        <h3><%hdl_headline/%></h3>
        <%IoRangeConditional%><h4><%stf_certificateInfo/%></h4><%/IoRangeConditional%>
        <%IoRangeConditional%><h4><%stf_aasInfo/%></h4><%/IoRangeConditional%>
        <%IoRangeConditional%><p><%txt_text%></p><%/IoRangeConditional%>"""
    },
    
    'Text - H3 (Main) Heading and Paragraph (with images)':
    {
        'html':"""            <h3><%hdl_headline/%></h3>
        <p><%txt_text/%><p>"""
    },
    
    'Text - H4 (Sub) Heading  and Paragraph (with images)':
    {
        'html':"""            <h4><%hdl_headline/%></h4>
        <p><%txt_text/%></p>"""
    },
    
    'Text - H4 (Sub) Heading and Paragraph (retractible)':
    {
        'html':"""
            <div class="dropper wrapper">
                <h4 class="dropControl"><%hdl_headline/%></h4>
                <div class="dropText"><%txt_text/%></div>
            </div>"""
    },
    
    'Gallery Page':
    {
        'html':"""
        <h4><%hdl_headline/%></h4>
        <%IoRangeConditional%><p><%txt_text/%></p><%/IoRangeConditional%>
        <div id="gallery" class="wrapper">
        <%IoRangeListContent%><%list_galleryImages/%><%/IoRangeListContent%>
        </div>"""
    },
    
    'Gallery Image':
    {
        'html':"""                <div class="gal_img">
                <a href="<%img_galleryImage/%>" title="<%stf_imageCaption/%>"><img src="<%img_galleryImage/%>" alt="<%hdl_headline/%>" border="0" /></a>
            </div>"""
    },
    
    'FAQs - List of FAQs':
    {
        'html':"""
            <h3><%hdl_headline/%></h3>
            <%IoRangeConditional%><p><%txt_faqDescription%></p><%/IoRangeConditional%>
            <%IoRangeListContent%><%list_faqs/%><%/IoRangeListContent%>"""
    },
    
    'Foundation - Single FAQ Page':
    {
        'html':"""
            <div class="faq_item wrapper">
                <div class="faq_question wrapper"><h4><%hdl_headline/%></h4></div>
                <div class="faq_answer wrapper"><%txt_text/%></div>
            </div>"""
    },
    
    'Links - File Download List (Two Columns)':
    {
        'html':"""
        <h4><%hdl_headline/%></h4>
        <%IoRangeConditional%><p><%txt_list_desc/%></p><%/IoRangeConditional%>
        <div class="two-column_links wrapper">
            <ul class="resources_links two-column_links_1 wrapper">
            <%IoRangeListContent%><%list_downloadItemPages1/%><%/IoRangeListContent%>
            </ul>
            <ul class="resources_links two-column_links_2 wrapper">
            <%IoRangeListContent%><%list_downloadItemPages2/%><%/IoRangeListContent%>
            </ul>
        </div>"""
    },
    
    'Links - File Download List and Image (One Column with Image)':
    {
        'html':"""
            <h4><%hdl_headline/%></h4>
            <%IoRangeConditional%><p><%txt_list_desc/%></p><%/IoRangeConditional%>
            <div id="links_and_image" class="wrapper">
                <ul class="resources_links two-column_links_1 wrapper">
                <%IoRangeListContent%><%list_downloadItemPages/%><%/IoRangeListContent%>
                </ul>
                <img src="<%img_linkListImage/%>" border="0" alt="" />
            </div>"""
    },
    
    'Downloads - Download Item':
    {#alternate title if you can get the meta elements: <%att_downloadFilename/%> (<%att_downloadFilesize/%> KB)">
        'html':"""
                    <li class="wrapper">
                        <a href="<%med_downloadFile/%>" title="<%hdl_headline/%>">
                            <span class="resources_links_span"><%hdl_headline/%></span>
                            <span class="rl_desc"><%stf_description/%></span> 
                        </a>
                    </li>"""
    },
    
    'Mapbox':
    {
        'html':"""            <h4><%hdl_headline/%></h4>
        <%IoRangeConditional%><p><%txt_text%><p><%/IoRangeConditional%>
        <div class="mapbox">
            <iframe width="625" height="300" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="<%IoRangeListLink%><%anc_googleMapIframeSourceLink%>anc_googleMapIframeSourceLink<%/anc_googleMapIframeSourceLink%><%/IoRangeListLink%>"></iframe>
        </div>"""
    },
    
    'anc_googleMapIframeSourceLink':
    {#hack for exportring list link with no export definition
        'html':"""<%anc_googleMapIframeSourceLink/%>"""
    },
    
    'flat text':
    {
        'html': 'Just some regular text to test in the parsing function.'
    }
}