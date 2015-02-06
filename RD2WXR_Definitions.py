#Handles WXR template generating with RedDot page elements
#To be imported for use in the RedLine Exporting function
#Auth Brys B 2014-12
#
#denote RedDot Elements by placeholders e.g. <%headline/%>
##placeholders cannot have whitespace
#
##simple place holders have trailing slash e.g. <%headline/%>
#
##placeholders for containers and lists have opening and closing tags
##e.g. <%IoRangeConditional%><%stf_description/%><%/IoRangeConditional%>
#
##Lists and containers must be nested e.g.
##<%IoRangeListLink%><%lst_listitems%>Item Definition Name - wxr item</li><%/lst_listitems%><%/IoRangeListLink%>
#
##Supported Containers: IoRangeConditional, IoRangeListLink, IoRangeListContent, IoRangeContainer
#
##IoRangeConditional can nest only one placeholder as argument
#
import datetime, re
import pprint

wordpresshost = 'http://philip.ozarkstech.org/'

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
	<generator>RedSuite v2.0</generator>"""
        #<wp:author><wp:author_id>2</wp:author_id>
        #<wp:author_login>brys</wp:author_login>
        #<wp:author_email>broughtb@otc.edu</wp:author_email>
        #<wp:author_display_name><![CDATA[Brys Broughton]]></wp:author_display_name>
        #<wp:author_first_name><![CDATA[Brys]]></wp:author_first_name><wp:author_last_name><![CDATA[Broughton]]></wp:author_last_name></wp:author>

footer = """</channel>
</rss>"""

wpds = {
    'Generic Foundation':
    {
        'html':
            """
            <wp:author>
                <wp:author_login><%createusername/%></wp:author_login>
                <wp:author_email><%createusername/%>@otc.edu</wp:author_email>
                <wp:author_display_name><![CDATA[<%createusername/%>]]></wp:author_display_name>
                <wp:author_first_name><![CDATA[First name not set]]></wp:author_first_name><wp:author_last_name><![CDATA[Last name not set]]></wp:author_last_name>
            </wp:author>
            <item>
            <title><%headline/%></title>
            <link>"""+wordpresshost+"""<%wp_filename/%></link>
            <pubDate></pubDate>
            <dc:creator><![CDATA[<%createusername/%>]]></dc:creator>
            <guid isPermaLink="false">"""+wordpresshost+"""<%wp_filename/%>/</guid>
            <description><%stf_metadescription/%></description>
            <content:encoded><![CDATA[
            <%IoRangeContainer%>con_body<%/IoRangeContainer%>
            <!-- Imported from RedDot Page<%id/%> -->
            ]]></content:encoded>
            <excerpt:encoded><![CDATA[<%stf_teaser/%>]]></excerpt:encoded>
		<wp:post_id></wp:post_id>
		<wp:post_date><%createdate/%></wp:post_date>
		<wp:post_date_gmt><%createdate/%></wp:post_date_gmt>
		<wp:comment_status>closed</wp:comment_status>
		<wp:ping_status>closed</wp:ping_status>
		<wp:post_name><%wp_filename/%></wp:post_name>
		<wp:status>publish</wp:status>
		<wp:post_parent></wp:post_parent>
		<wp:menu_order>1</wp:menu_order>
		<wp:post_type>page</wp:post_type>
		<wp:post_password></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<wp:postmeta>
			<wp:meta_key>_wp_page_template</wp:meta_key>
			<wp:meta_value><![CDATA[default]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key>_edit_last</wp:meta_key>
			<wp:meta_value><![CDATA[2]]></wp:meta_value>
		</wp:postmeta>
            </item>
            """
    },
    
    'Generic Sub Foundation':
    {
        'html':
            """
            <wp:author>
                <wp:author_login><%createusername/%></wp:author_login>
                <wp:author_email><%createusername/%>@otc.edu</wp:author_email>
                <wp:author_display_name><![CDATA[<%createusername/%>]]></wp:author_display_name>
                <wp:author_first_name><![CDATA[First name not set]]></wp:author_first_name><wp:author_last_name><![CDATA[Last name not set]]></wp:author_last_name>
            </wp:author>
            <item>
            <title><%headline/%></title>
            <link>"""+wordpresshost+"""<%wp_filename/%></link>
            <pubDate></pubDate>
            <dc:creator><![CDATA[<%createusername/%>]]></dc:creator>
            <guid isPermaLink="false">"""+wordpresshost+"""<%wp_filename/%>/</guid>
            <description><%stf_metadescription/%></description>
            <content:encoded><![CDATA[
            <%IoRangeContainer%>con_body<%/IoRangeContainer%>
            <!-- Imported from RedDot Page<%id/%> -->
            ]]></content:encoded>
            <excerpt:encoded><![CDATA[<%stf_teaser/%>]]></excerpt:encoded>
		<wp:post_id></wp:post_id>
		<wp:post_date><%createdate/%></wp:post_date>
		<wp:post_date_gmt><%createdate/%></wp:post_date_gmt>
		<wp:comment_status>closed</wp:comment_status>
		<wp:ping_status>closed</wp:ping_status>
		<wp:post_name><%wp_filename/%></wp:post_name>
		<wp:status>publish</wp:status>
		<wp:post_parent><%wp_parentid/%></wp:post_parent>
		<wp:menu_order>1</wp:menu_order>
		<wp:post_type>page</wp:post_type>
		<wp:post_password></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<wp:postmeta>
			<wp:meta_key>_wp_page_template</wp:meta_key>
			<wp:meta_value><![CDATA[default]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key>_edit_last</wp:meta_key>
			<wp:meta_value><![CDATA[2]]></wp:meta_value>
		</wp:postmeta>
            </item>
            """
    },
    
    'Foundation - Single Article':
    {
        'html':"""
        <wp:author>
            <wp:author_login><%createusername/%></wp:author_login>
            <wp:author_email><%createusername/%>@otc.edu</wp:author_email>
            <wp:author_display_name><![CDATA[<%createusername/%>]]></wp:author_display_name>
            <wp:author_first_name><![CDATA[First name not set]]></wp:author_first_name><wp:author_last_name><![CDATA[Last name not set]]></wp:author_last_name>
        </wp:author>
	<item>
		<title><%headline/%></title>
                <link>http://philip.ozarkstech.org</link>
		<pubDate></pubDate>
		<dc:creator><![CDATA[<%createusername/%>]]></dc:creator>
		<guid isPermaLink="false">http://philip.ozarkstech.org/</guid>
		<description><%stf_metadescription/%></description>
		<content:encoded><![CDATA[
                    <%IoRangeConditional%><div class="pr_imagewrapper"><img src="<%img_image/%>" /></div><%/IoRangeConditional%>
                    <%txt_text/%>
                    <%IoRangeContainer%>con_body<%/IoRangeContainer%>
                    <div class="contributors_box">
                        <div class="contributors_inner">
                            <h3>Contributors</h3>
                            <div class="contributor">
                                <h4><%stf_mediaContactName1/%></h4>
                                <h5 class="title"><%stf_mediaContactTitle1/%></h5>
                                <p>Phone: <%stf_mediaContactPhone1/%></p>
                                <p>Email: <%stf_mediaContactEmail1/%></p>
                            </div>
                            <div class="contributor">
                                <h4><%stf_mediaContactName2/%></h4>
                                <h5 class="title"><%stf_mediaContactTitle2/%></h5>
                                <p>Phone: <%stf_mediaContactPhone2/%></p>
                                <p>Email: <%stf_mediaContactEmail2/%></p>
                            </div>
                            <div class="contributor">
                                <h4><%stf_mediaContactName3/%></h4>
                                <h5 class="title"><%stf_mediaContactTitle3/%></h5>
                                <%IoRangeConditional%><p>Phone: <%stf_mediaContactPhone3/%></p><%/IoRangeConditional%>
                                <%IoRangeConditional%><p>Email: <%stf_mediaContactEmail3/%></p><%/IoRangeConditional%>
                            </div>
                            <div class="contributor">
                                <h4><%stf_mediaContactName4/%></h4>
                                <h5 class="title"><%stf_mediaContactTitle4/%></h5>
                                <%IoRangeConditional%><p>Phone: <%stf_mediaContactPhone4/%></p><%/IoRangeConditional%>
                                <%IoRangeConditional%><p>Email: <%stf_mediaContactEmail4/%></p><%/IoRangeConditional%>
                            </div>
                        </div>
                    </div>
                    <!-- Imported from RedDot Page<%id/%> -->
                ]]></content:encoded>
		<excerpt:encoded><![CDATA[<%stf_teaser/%>]]></excerpt:encoded>
		<wp:post_id></wp:post_id>
		<wp:post_date><%createdate/%></wp:post_date>
		<wp:post_date_gmt><%createdate/%></wp:post_date_gmt>
		<wp:comment_status>closed</wp:comment_status>
		<wp:ping_status>closed</wp:ping_status>
		<wp:post_name><%wp_filename/%></wp:post_name>
		<wp:status>publish</wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type>post</wp:post_type>
		<wp:post_password></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<category domain="category" nicename="News Releases"><![CDATA[news releases]]></category>
		<wp:postmeta>
			<wp:meta_key>_edit_last</wp:meta_key>
			<wp:meta_value><![CDATA[2]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key>_thumbnail_id</wp:meta_key>
			<wp:meta_value><![CDATA[7]]></wp:meta_value>
		</wp:postmeta>
	</item>
        """
    },
    
    'Foundation - Single Press Release':
    {
        'html':"""
        <wp:author>
            <wp:author_login><%createusername/%></wp:author_login>
            <wp:author_email><%createusername/%>@otc.edu</wp:author_email>
            <wp:author_display_name><![CDATA[<%createusername/%>]]></wp:author_display_name>
            <wp:author_first_name><![CDATA[First name not set]]></wp:author_first_name><wp:author_last_name><![CDATA[Last name not set]]></wp:author_last_name>
        </wp:author>
	<item>
		<title><%headline/%></title>
                <link>http://philip.ozarkstech.org</link>
		<pubDate></pubDate>
		<dc:creator><![CDATA[<%createusername/%>]]></dc:creator>
		<guid isPermaLink="false">http://philip.ozarkstech.org/</guid>
		<description><%stf_metadescription/%></description>
		<content:encoded><![CDATA[
                    <%IoRangeConditional%><div class="pr_imagewrapper"><img src="<%img_image/%>" /></div><%/IoRangeConditional%>
                    <%txt_text/%>
                    <%IoRangeContainer%>con_body<%/IoRangeContainer%>
                    <div class="contributors_box">
                        <div class="contributors_inner">
                            <h3>Contributors</h3>
                            <div class="contributor">
                                <h4><%stf_mediaContactName1/%></h4>
                                <h5 class="title"><%stf_mediaContactTitle1/%></h5>
                                <p>Phone: <%stf_mediaContactPhone1/%></p>
                                <p>Email: <%stf_mediaContactEmail1/%></p>
                            </div>
                            <div class="contributor">
                                <h4><%stf_mediaContactName2/%></h4>
                                <h5 class="title"><%stf_mediaContactTitle2/%></h5>
                                <p>Phone: <%stf_mediaContactPhone2/%></p>
                                <p>Email: <%stf_mediaContactEmail2/%></p>
                            </div>
                            <div class="contributor">
                                <h4><%stf_mediaContactName3/%></h4>
                                <h5 class="title"><%stf_mediaContactTitle3/%></h5>
                                <%IoRangeConditional%><p>Phone: <%stf_mediaContactPhone3/%></p><%/IoRangeConditional%>
                                <%IoRangeConditional%><p>Email: <%stf_mediaContactEmail3/%></p><%/IoRangeConditional%>
                            </div>
                            <div class="contributor">
                                <h4><%stf_mediaContactName4/%></h4>
                                <h5 class="title"><%stf_mediaContactTitle4/%></h5>
                                <%IoRangeConditional%><p>Phone: <%stf_mediaContactPhone4/%></p><%/IoRangeConditional%>
                                <%IoRangeConditional%><p>Email: <%stf_mediaContactEmail4/%></p><%/IoRangeConditional%>
                            </div>
                        </div>
                    </div>
                    <!-- Imported from RedDot Page<%id/%> -->
                ]]></content:encoded>
		<excerpt:encoded><![CDATA[<%stf_teaser/%>]]></excerpt:encoded>
		<wp:post_id></wp:post_id>
		<wp:post_date><%createdate/%></wp:post_date>
		<wp:post_date_gmt><%createdate/%></wp:post_date_gmt>
		<wp:comment_status>closed</wp:comment_status>
		<wp:ping_status>closed</wp:ping_status>
		<wp:post_name><%wp_filename/%></wp:post_name>
		<wp:status>publish</wp:status>
		<wp:post_parent>0</wp:post_parent>
		<wp:menu_order>0</wp:menu_order>
		<wp:post_type>post</wp:post_type>
		<wp:post_password></wp:post_password>
		<wp:is_sticky>0</wp:is_sticky>
		<category domain="category" nicename="Press Releases"><![CDATA[press releases]]></category>
		<wp:postmeta>
			<wp:meta_key>_edit_last</wp:meta_key>
			<wp:meta_value><![CDATA[2]]></wp:meta_value>
		</wp:postmeta>
		<wp:postmeta>
			<wp:meta_key>_thumbnail_id</wp:meta_key>
			<wp:meta_value><![CDATA[7]]></wp:meta_value>
		</wp:postmeta>
	</item>
        """
    },
    
    #'Foundation - Wide Image Page':
    #{ #cancelled - can't set feature image, has to be manually done
    #    'html':"""NEEDS DEFINITION"""#needs to set feature image
    #},
    
    'Links - File Download List (One Column)':
    {
        'html':"""NEEDS DEFINITION"""
    },
    
    'PR - Article Table':
    {
        'html':"""NEEDS DEFINITION"""
    },
    
    'PR - Press Release Table':
    {
        'html':"""NEEDS DEFINITION"""
    },
    
    'Text - H4 (Sub) Heading  and Paragraph':
    {
        'html':"""NEEDS DEFINITION"""
    },
    
    'Videos - Vimeo Video Page':
    {
        'html':"""NEEDS DEFINITION"""
    },
    
    'Navigation Connector':
    {
        'html':""""""#no output for these
    },
    
    'Text - H3 (Main) Heading and Paragraph':
    {
        'html':"""<h3><%headline/%></h3>\n<div><%txt_text/%></div>"""
        
    },
    
    'Links - Large Bulleted Link List (Two Columns)':
    {
        'html':"""
            <h4><%headline/%></h4>
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
        'html':"""<li><a href="<%URL/%>"><span class="big_links_span"><%headline/%></span></a></li>\n"""
    },
    
    'Links - Small Bulleted Link List (Two Columns)':
    {
        'html':"""
            <h4><%headline/%></h4>
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
        'html':"""<li><a href="<%URL/%>"><span class="feature_links_span"><%headline/%></span></a></li>\n"""
    },
    
    'Bio Box (Large)':
    {
        'html':"""
            <div class="content_bio_box_large wrapper">
                <img src="<%img_bioImage/%>" border="0" alt="<%headline/%>" class="content_bio_image" />
                <div class="content_bio_info wrapper">
                    <a href="mailto:<%stf_email/%>" class="mail_icon" title="Email <%headline/%>"><span>Email <%headline/%></span></a>
                    <h3><%headline/%></h3>
                    <%IoRangeConditional%><h4><%stf_positionTitle/%></h4><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree1/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree2/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree3/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree4/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree5/%></h5><%/IoRangeConditional%>"""+
                    #<%IoRangeConditionalAnchor%><%anc_website%>Bio Box (Large) - wxr item - website link<%/anc_website%><%/IoRangeConditionalAnchor%>
                    """<%IoRangeConditional%><h5 class="highlight-blue">Office: <%stf_officeNumber/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5 class="highlight-blue">Phone: <%stf_phoneNumber/%></h5><%/IoRangeConditional%>
                </div>
                <%IoRangeConditional%><%txt_text/%><%/IoRangeConditional%>
            </div>"""
    },
    
    'Bio Box (Large) - wxr item - bio image':
    {
        'html':"""<img src="<%img_bioImage/%>" border="0" alt="<%headline/%>" class="content_bio_image" />"""
    },
    
    'Bio Box (Large) - wxr item - website link':
    {
        'html':"""<h5><a href="<%anc_website/%>" title="<%stf_websiteTitle/%>" target="_blank" class="bio_link"><%stf_websiteTitle/%></a></h5>"""
    },
    
    'Bio Box (Small)':
    {
        'html':"""                <div class="content_bio_box wrapper">
                <img src="<%img_bioImage/%>" border="0" alt="<%headline/%>" class="content_bio_image" />
                <div class="content_bio_info boxes wrapper">
                    <a href="mailto:<%stf_email/%>" class="mail_icon" title="Email <%headline/%>"><span>Email <%headline/%></span></a>
                    <h3><%headline/%></h3>
                    <h4><%stf_positionTitle/%></h4>
                    <%IoRangeConditional%><h5><%stf_degree1/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree2/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree3/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree4/%></h5><%/IoRangeConditional%>
                    <%IoRangeConditional%><h5><%stf_degree5/%></h5><%/IoRangeConditional%>"""+
                    #<%IoRangeConditionalAnchor%><%anc_website%>Bio Box (Small) - wxr item - website link<%/anc_website%><%/IoRangeConditionalAnchor%>
                    """<h4 class="highlight-blue">
                        <%IoRangeConditional%>Office: <%stf_officeNumber%><%/IoRangeConditional%>
                        <%IoRangeConditional%>Phone: <%stf_phoneNumber%><%/IoRangeConditional%>
                    </h4>
                </div>                            
                <%IoRangeConditional%><%txt_text%><%/IoRangeConditional%>
            </div>"""
    },
    
    'Bio Box (Small) - wxr item - website link':
    {
        'html':"""<h5><a href="<%anc_website/%>" title="<%stf_websiteTitle/%>" target="_blank" class="bio_link"><%stf_websiteTitle/%></a></h5>"""
    },
    
    'Catalog - Program Overview':
    {
        'html':"""
        <h3><%headline/%></h3>
        <%IoRangeConditional%><h4><%stf_certificateInfo/%></h4><%/IoRangeConditional%>
        <%IoRangeConditional%><h4><%stf_aasInfo/%></h4><%/IoRangeConditional%>
        <%IoRangeConditional%><p><%txt_text%></p><%/IoRangeConditional%>"""
    },
    
    'Text - H3 (Main) Heading and Paragraph (with images)':
    {
        'html':"""            <h3><%headline/%></h3>
        <%txt_text/%>"""
    },
    
    'Text - H4 (Sub) Heading  and Paragraph (with images)':
    {
        'html':"""            <h4><%headline/%></h4>
        <%txt_text/%>"""
    },
    
    'Text - H4 (Sub) Heading and Paragraph (retractible)':
    {
        'html':"""
            <div class="dropper wrapper">
                <h4 class="dropControl"><%headline/%></h4>
                <div class="dropText"><%txt_text/%></div>
            </div>"""
    },
    
    'Gallery Page':
    {
        'html':"""
        <h4><%headline/%></h4>
        <%IoRangeConditional%><div class="gallery_desc"><%txt_text/%></div><%/IoRangeConditional%>
        <div id="gallery" class="wrapper">
        <%IoRangeListContent%>list_galleryImages<%/IoRangeListContent%>
        </div>"""
    },
    
    'Gallery Image':
    {
        'html':"""                <div class="gal_img">
                <a href="<%img_galleryImage/%>" title="<%stf_imageCaption/%>"><img src="<%img_galleryImage/%>" alt="<%headline/%>" border="0" /></a>
            </div>"""
    },
    
    'FAQs - List of FAQs':
    {
        'html':"""
            <h3><%headline/%></h3>
            <%IoRangeConditional%><div><%txt_faqDescription/%></div><%/IoRangeConditional%>
            <%IoRangeListContent%>list_faqs<%/IoRangeListContent%>"""
    },
    
    'Foundation - Single FAQ Page':
    {
        'html':"""
            <div class="faq_item wrapper">
                <div class="faq_question wrapper"><h4><%headline/%></h4></div>
                <div class="faq_answer wrapper"><%txt_text/%></div>
            </div>"""
    },
    
    'Links - File Download List (Two Columns)':
    {
        'html':"""
        <h4><%headline/%></h4>
        <%IoRangeConditional%><p><%txt_list_desc/%></p><%/IoRangeConditional%>
        <div class="two-column_links wrapper">
            <ul class="resources_links two-column_links_1 wrapper">
            <%IoRangeListContent<%list_downloadItemPages1<%/IoRangeListContent%>
            </ul>
            <ul class="resources_links two-column_links_2 wrapper">
            <%IoRangeListContent<%list_downloadItemPages2<%/IoRangeListContent%>
            </ul>
        </div>"""
    },
    
    'Links - File Download List and Image (One Column with Image)':
    {
        'html':"""
            <h4><%headline/%></h4>
            <img src="<%img_linkListImage/%>" border="0" alt="" />
            <%IoRangeConditional%><p><%txt_list_desc/%></p><%/IoRangeConditional%>
            <div id="links_and_image" class="wrapper">
                <ul class="resources_links two-column_links_1 wrapper">
                <%IoRangeListContent%>list_downloadItemPages<%/IoRangeListContent%>
                </ul>
            </div>"""
    },
    
    'Downloads - Download Item':
    {#alternate title if you can get the meta elements: <%att_downloadFilename/%> (<%att_downloadFilesize/%> KB)">
        'html':"""
                    <li class="wrapper">
                        <a href="<%med_downloadFile/%>" title="<%headline/%>">
                            <span class="resources_links_span"><%headline/%></span>
                            <span class="rl_desc"><%stf_description/%></span> 
                        </a>
                    </li>"""
    },
    
    'Mapbox':
    {
        'html':
            """
        <h4><%headline/%></h4>
        <%IoRangeConditional%><div class="map_desc"><%txt_text/%></div><%/IoRangeConditional%>
        <div class="mapbox">
            <iframe width="625" height="300" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://www.google.com/maps/place/Ozarks+Technical+Community+College/@37.2144019,-93.2825409,15z/data=!4m2!3m1!1s0x0000000000000000:0x76db2ff4de702b77"></iframe>
        </div>"""
    },
    
    'anc_googleMapIframeSourceLink':
    {#Content class uses assigned urls, which are unrecoverable. Just give all maps OTC map for now
        'html':"""https://www.google.com/maps/place/Ozarks+Technical+Community+College/@37.2144019,-93.2825409,15z/data=!4m2!3m1!1s0x0000000000000000:0x76db2ff4de702b77"""
    },
    
   
    'flat text':
    {
        'html': 'Just some regular text to test in the parsing function.'
    }
}

def parse(wpdef):
    """
    Returns mixed list representing abstract syntax tree.
    List may contain strings or tuples.
    Strings are basic ouput.
    Tuples are function calls.
    (fname, nestedwxr)
    """
    #pprint.pprint(wpdef)
    tokens = re.split('<%\s*|\s*%>', wpdef, 2)
    #pprint.pprint(tokens)
    
    if len(tokens) == 1:
        return tokens #finished parsing
    
    if len(tokens) is not 3:
        raise Exception('Parse Error: mis-matched "<%" or %>')
    
    #tokens = filter(lambda x: x, tokens)#removes empty strings
    ast = []
    
    #simple self-closing placeholder
    if tokens[1].endswith('/'):
        ast = [tokens[0], ('placeholder', tokens[1][:-1])] + parse(tokens[2])
        #ast= [text, ('getplaceholder', tag)] + parse(text)
    elif tokens[1].startswith('/'):
        raise Exception('Parse Error: mis-matched end tag at ' + tokens[1])
    else:#opening placeholder
        subtokens = re.split('<%/'+tokens[1]+'%>', tokens[2], 1)
        if len(subtokens) < 2:
            raise Exception("Parse Error: Missing closing placeholder: " + tokens[1])
        ast = [tokens[0], (tokens[1] ,subtokens[0])] + parse(subtokens[1])
        #ast= [text, (tag, innertext)] + parse(text)
        
    return ast#filter(lambda)
        
    