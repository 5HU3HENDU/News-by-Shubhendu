import streamlit as st
import feedparser
from datetime import datetime

st.title("RSS Feed Reader")

# Input for multiple RSS feed URLs
feed_urls = """
https://alphaideas.in/feed/
https://entrackr.com/rss
https://factordaily.com/feed/
https://feeds.bbci.co.uk/news/world/asia/rss.xml
https://finshots.in/rss/
https://gfmag.com/feed/
https://prod-qt-images.s3.amazonaws.com/production/bloombergquint/feed.xml
https://qz.com/rss
https://restofworld.org/feed/latest/
https://techcrunch.com/feed/
https://technode.com/feed/
https://the420.in/feed/
https://the-ken.com/feed/
https://tldr.tech/api/rss/tech
https://www.densediscovery.com/feed/
https://www.exponentialview.co/feed
https://www.forbesindia.com/commonfeeds/v1/frb/rss/news.xml
https://www.hindustantimes.com/feeds/rss/business/rssfeed.xml
https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml
https://www.hindustantimes.com/feeds/rss/technology/rssfeed.xml
https://www.techinasia.com/feed
https://www.technologyreview.com/feed/
https://www.theinformation.com/feed/
https://www.wired.com/feed/

"""

# Single date picker for day selection
selected_date = st.date_input("Select Date:", datetime.now())

if feed_urls:
    urls = [url.strip() for url in feed_urls.split("\n") if url.strip()]

    if urls:
        all_articles = []

        for url in urls:
            try:
                feed = feedparser.parse(url)
                feed_title = feed.feed.title if hasattr(feed.feed, 'title') else url

                for entry in feed.entries:
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6])

                        # Filter by selected date
                        if pub_date.date() == selected_date:
                            all_articles.append({
                                'feed': feed_title,
                                'title': entry.title,
                                'link': entry.link,
                                'time': pub_date.strftime('%H:%M'),
                                'datetime': pub_date
                            })
            except:
                pass

        # Sort by time
        all_articles.sort(key=lambda x: x['datetime'], reverse=True)

        if all_articles:
            st.success(f"Found {len(all_articles)} articles for {selected_date.strftime('%B %d, %Y')}")

            for article in all_articles:
                st.subheader(article['title'])
                st.write(f" :alarm_clock: {article['time']} | :newspaper: {article['feed']}")
                st.markdown(f"[Read more :link:]({article['link']})")
                st.divider()
        else:
            st.info(f"No articles found for {selected_date.strftime('%B %d, %Y')}")


