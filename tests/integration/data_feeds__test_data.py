TEST_DATA__HACKER_NEWS__FEED_XML = '''<?xml version="1.0" encoding="UTF-8"?>
                                      <rss version="2.0" xmlns:sy="http://purl.org/rss/1.0/modules/syndication/">
                                          <channel>
                                              <title>The Hacker News</title>
                                              <link>https://thehackernews.com</link>
                                              <description>Security News</description>
                                              <language>en-us</language>
                                              <lastBuildDate>Thu, 05 Dec 2024 01:33:01 +0530</lastBuildDate>
                                              <sy:updatePeriod>hourly</sy:updatePeriod>
                                              <sy:updateFrequency>1</sy:updateFrequency>
                                              <item>
                                                  <title>Test Article</title>
                                                  <description><![CDATA[Test Description]]></description>
                                                  <link>https://thehackernews.com/2024/12/test-article.html</link>
                                                  <guid>https://thehackernews.com/2024/12/test-article.html</guid>
                                                  <pubDate>Wed, 04 Dec 2024 22:53:00 +0530</pubDate>
                                                  <author>info@thehackernews.com (The Hacker News)</author>
                                                  <enclosure url="https://example.com/image.jpg" type="image/jpeg" length="12216320"/>
                                              </item>
                                          </channel>
                                      </rss>'''

TEST_DATA__SECURITY_NEWS__FEED_XML = '''<?xml version="1.0" encoding="UTF-8"?>
                                        <rss version="2.0"
                                            xmlns:content="http://purl.org/rss/1.0/modules/content/"
                                            xmlns:wfw="http://wellformedweb.org/CommentAPI/"
                                            xmlns:dc="http://purl.org/dc/elements/1.1/"
                                            xmlns:atom="http://www.w3.org/2005/Atom"
                                            xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
                                            xmlns:slash="http://purl.org/rss/1.0/modules/slash/">
                                        
                                        <channel>
                                            <title>Sample Security News</title>
                                            <atom:link href="https://www.samplesecuritynews.com/feed/" rel="self" type="application/rss+xml" />
                                            <link>https://www.samplesecuritynews.com/</link>
                                            <description>Cybersecurity News, Insights &amp; Analysis</description>
                                            <lastBuildDate>Mon, 23 Dec 2024 14:00:00 +0000</lastBuildDate>
                                            <language>en-US</language>
                                            <sy:updatePeriod>hourly</sy:updatePeriod>
                                            <sy:updateFrequency>1</sy:updateFrequency>
                                            <generator>Sample Generator v1.0</generator>
                                        
                                            <image>
                                                <url>https://www.samplesecuritynews.com/logo.png</url>
                                                <title>Sample Security News</title>
                                                <link>https://www.samplesecuritynews.com/</link>
                                                <width>32</width>
                                                <height>32</height>
                                            </image>
                                        
                                            <item>
                                                <title>Understanding Shadow AI in Cybersecurity</title>
                                                <link>https://www.samplesecuritynews.com/shadow-ai/</link>
                                                <dc:creator><![CDATA[John Doe]]></dc:creator>
                                                <pubDate>Mon, 23 Dec 2024 13:00:00 +0000</pubDate>
                                                <category><![CDATA[Artificial Intelligence]]></category>
                                                <category><![CDATA[Cybersecurity]]></category>
                                                <guid isPermaLink="false">https://www.samplesecuritynews.com/shadow-ai-article</guid>
                                                <description><![CDATA[<p>Explore the risks and opportunities of Shadow AI in modern cybersecurity environments.</p>
                                        <p>The post <a href="https://www.samplesecuritynews.com/shadow-ai/">Understanding Shadow AI in Cybersecurity</a> appeared first on <a href="https://www.samplesecuritynews.com/">Sample Security News</a>.</p>]]></description>
                                            </item>
                                        
                                            <item>
                                                <title>Top 5 Cyber Threats to Watch in 2025</title>
                                                <link>https://www.samplesecuritynews.com/top-cyber-threats-2025/</link>
                                                <dc:creator><![CDATA[Jane Smith]]></dc:creator>
                                                <pubDate>Mon, 23 Dec 2024 12:00:00 +0000</pubDate>
                                                <category><![CDATA[Cyber Threats]]></category>
                                                <category><![CDATA[Forecast]]></category>
                                                <guid isPermaLink="false">https://www.samplesecuritynews.com/cyber-threats-2025</guid>
                                                <description><![CDATA[<p>A deep dive into the emerging cyber threats of 2025 and how to prepare for them.</p>
                                        <p>The post <a href="https://www.samplesecuritynews.com/top-cyber-threats-2025/">Top 5 Cyber Threats to Watch in 2025</a> appeared first on <a href="https://www.samplesecuritynews.com/">Sample Security News</a>.</p>]]></description>
                                            </item>
                                        
                                        </channel>
                                        </rss>
                                        '''