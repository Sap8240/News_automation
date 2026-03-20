import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime, timedelta
import time
import requests
from bs4 import BeautifulSoup
import re
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# Your existing RSS feeds & keywords (same as bot)
RSS_FEEDS = {
    "NDTV Breaking": "https://feeds.feedburner.com/ndtvnews-latest",
    "NDTV Top": "https://feeds.feedburner.com/ndtvnews-top-stories",
    "NDTV India": "https://feeds.feedburner.com/ndtvnews-india-news",
    "India Today": "https://www.indiatoday.in/rss/home",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",

    # === LEGAL / COURTS / JUSTICE ===
    "Indian Express": "https://indianexpress.com/section/india/feed/",
    "The Hindu India": "https://www.thehindu.com/news/national/feed/",
    "Scroll India": "https://scroll.in/latest.rss",

    # === YOUTH / EDUCATION / STUDENTS ===
    "The Print": "https://theprint.in/feed/",
    "The Wire": "https://thewire.in/feed/",

    # === ECONOMY / JOBS / INFRA ===
    "Mint": "https://www.livemint.com/rss/home-page",
    "Economic Times": "https://economictimes.indiatimes.com/rssfeedstopstories.cms",

    # === ENVIRONMENT / DISASTERS ===
    "DownToEarth": "https://www.downtoearth.org.in/rss",

    # === AGGREGATORS ===
    "Google News India": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en",
    "BBC India": "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
}

PRIORITY_KEYWORDS = [
    "rape", "gangrape", "sexual assault", "domestic violence", "dowry death",
    "acid attack", "honour killing", "lynching", "mob lynching",
    "student suicide", "student protest", "campus protest", "hostel protest",
    "exam leak", "paper leak", "neet", "jee", "upsc", "coaching centre",
    "police brutality", "lathicharge", "custodial death", "police firing",
    "bridge collapse", "flyover collapse", "building collapse", "train derailment",
    "supreme court", "high court", "bail denied", "bail granted", "sentenced",
    "farmer suicide", "farmers protest", "farmers march"
]

TRENDING_KEYWORDS = [
    "parliament", "lok sabha", "rajya sabha", "election", "by-election",
    "modi", "prime minister", "cm", "chief minister", "mla", "mp",
    "cbi raid", "ed raid", "income tax raid", "scam", "corruption",
    "unemployment", "jobless", "layoffs", "inflation", "fuel price",
    "petrol price", "diesel price", "gst hike", "reservation", "quota",
    "smart city", "infrastructure failure", "waterlogging", "flooded streets",
    "pollution", "aqi", "smog", "toxic air", "heatwave", "cold wave",
    "dalit", "tribal", "adivasi", "moral policing", "cag report"
]

BREAKING_KEYWORDS = ["breaking", "urgent", "just in", "exclusive", "live updates",
    "alert", "developing", "developing story"]

st.set_page_config(
    page_title="TheIndianVisual News Dashboard",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced TheIndianVisual branding with better styling
st.markdown("""
    <style>
    .main-header {
        color: #0E1733; 
        font-size: 3rem; 
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .priority {
        background: linear-gradient(90deg, #FF4444, #CC0000); 
        color: white; 
        padding: 6px 12px; 
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .trending {
        background: linear-gradient(90deg, #FFD700, #FFA500); 
        color: black; 
        padding: 6px 12px; 
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .regular {
        background: #28A745; 
        color: white; 
        padding: 6px 12px; 
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        text-align: center;
    }
    .news-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: transform 0.2s, box-shadow 0.2s;
        margin-bottom: 1.5rem;
    }
    .news-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    .news-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #e81109;
        margin-bottom: 0.8rem;
        line-height: 1.4;
    }
    .news-meta {
        display: flex;
        gap: 1rem;
        margin-bottom: 1rem;
        flex-wrap: wrap;
        font-size: 0.9rem;
    }
    .news-meta-item {
        background: #f0f2f6;
        padding: 4px 10px;
        border-radius: 20px;
        color: #666;
    }
    .news-image {
        width: 100%;
        height: 250px;
        object-fit: cover;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .news-summary {
        color: #d1d1d1;
        line-height: 1.6;
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .read-more {
        display: inline-block;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        transition: transform 0.2s;
    }
    .read-more:hover {
        transform: scale(1.05);
    }
    .stats-section {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar configuration
st.sidebar.title("⚙️ Dashboard Settings")

with st.sidebar.expander("🔍 Filters & Search", expanded=True):
    st.sidebar.subheader("Refresh Settings")
    refresh_interval = st.sidebar.slider("Auto-refresh (seconds)", 30, 600, 120)
    
    # Real auto-refresh component
    st_autorefresh(interval=refresh_interval * 1000, key="newsfeedrefresh")
    
    keyword_filter = st.sidebar.text_input("🔎 Search Keywords", "")
    
    st.sidebar.subheader("News Categories")
    show_priority = st.sidebar.checkbox("🔴 Show Priority News", value=True)
    show_trending = st.sidebar.checkbox("🟡 Show Trending News", value=True)
    show_regular = st.sidebar.checkbox("🟢 Show Regular News", value=False)

with st.sidebar.expander("📊 Data Settings"):
    max_stories = st.sidebar.slider("Max stories per source", 5, 20, 10)
    st.sidebar.info(f"Showing up to {max_stories} stories per source")

# Quick action buttons
st.sidebar.markdown("---")
col_refresh, col_clear = st.sidebar.columns(2)
with col_refresh:
    if st.button("🔄 Refresh Now", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

with col_clear:
    if st.button("🗑️ Clear Cache", use_container_width=True):
        st.cache_data.clear()
        st.info("Cache cleared!")

# Stats sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Quick Stats")
st.sidebar.metric("Total Feed Sources", len(RSS_FEEDS))
st.sidebar.metric("Priority Keywords", len(PRIORITY_KEYWORDS))
st.sidebar.metric("Trending Keywords", len(TRENDING_KEYWORDS))

# Last update time placeholder will be filled later
last_update_placeholder = st.sidebar.empty()

def extract_image_from_entry(entry):
    """Extract image URL from RSS entry"""
    image_url = None
    
    # Try media:content
    if hasattr(entry, 'media_content') and entry.media_content:
        for media in entry.media_content:
            if media.get('type', '').startswith('image'):
                return media.get('url')
    
    # Try enclosures
    if hasattr(entry, 'enclosures') and entry.enclosures:
        for enc in entry.enclosures:
            if 'image' in enc.get('type', ''):
                return enc.get('href')
    
    # Try image tag in summary
    if hasattr(entry, 'summary') and entry.summary:
        soup = BeautifulSoup(entry.summary, 'html.parser')
        img = soup.find('img')
        if img and img.get('src'):
            return img.get('src')
        
        # Try background-image
        for tag in soup.find_all():
            if tag.get('style') and 'background-image' in tag.get('style', ''):
                match = re.search(r'url\([\'"]?([^\)\'\"]+)[\'"]?\)', tag.get('style'))
                if match:
                    return match.group(1)
    
    return image_url

@st.cache_data(ttl=60)  # Cache for 1 minute
def fetch_news():
    all_news = []
    fetch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for source, url in RSS_FEEDS.items():
        try:
            # Using requests to bypass potential feedparser/WAF issues
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:10]:
                # Extract full summary (better than truncated version)
                summary = getattr(entry, 'summary', '')
                # Remove HTML tags
                summary_clean = BeautifulSoup(summary, 'html.parser').get_text()[:400]
                
                news_item = {
                    'title': entry.title,
                    'link': entry.link,
                    'source': source,
                    'published': entry.get('published', 'Just now'),
                    'summary': summary_clean + ('...' if len(summary_clean) >= 400 else ''),
                    'image': extract_image_from_entry(entry),
                    'author': entry.get('author', 'Unknown'),
                }
                
                # Classify priority
                text = (entry.title + " " + summary).lower()
                if any(kw in text for kw in BREAKING_KEYWORDS):
                    news_item['priority'] = '🔴 PRIORITY'
                elif any(kw in text for kw in PRIORITY_KEYWORDS):
                    news_item['priority'] = '🔴 PRIORITY'
                elif any(kw in text for kw in TRENDING_KEYWORDS):
                    news_item['priority'] = '🟡 TRENDING'
                else:
                    news_item['priority'] = '🟢 REGULAR'
                
                all_news.append(news_item)
        except Exception as e:
            st.sidebar.warning(f"Error fetching from {source}: {str(e)[:50]}")
            continue
    
    return {
        'news': sorted(all_news, key=lambda x: x['priority'], reverse=True),
        'time': fetch_time
    }

def display_news_card(story):
    """Display a formatted news card with image and details"""
    with st.container():
        # Priority badge and source
        col1, col2 = st.columns([1, 5])
        with col1:
            if story['priority'] == '🔴 PRIORITY':
                st.markdown('<div class="priority">🔴 PRIORITY</div>', unsafe_allow_html=True)
            elif story['priority'] == '🟡 TRENDING':
                st.markdown('<div class="trending">🟡 TRENDING</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="regular">🟢 REGULAR</div>', unsafe_allow_html=True)
        
        # Title
        st.markdown(f'<div class="news-title">{story["title"]}</div>', unsafe_allow_html=True)
        
        # Meta information
        meta_html = f'''
        <div class="news-meta">
            <span class="news-meta-item">📰 {story['source']}</span>
            <span class="news-meta-item">⏰ {story['published']}</span>
            {'<span class="news-meta-item">✍️ ' + story['author'] + '</span>' if story.get('author') and story['author'] != 'Unknown' else ''}
        </div>
        '''
        st.markdown(meta_html, unsafe_allow_html=True)
        
        # Display image if available
        if story.get('image'):
            try:
                st.image(story['image'], use_column_width=True, caption="News Image")
            except:
                pass  # Image loading failed, continue without it
        
        # Summary
        st.markdown(f'<div class="news-summary">{story["summary"]}</div>', unsafe_allow_html=True)
        
        # Read more link
        st.markdown(
            f'<a href="{story["link"]}" target="_blank" class="read-more">📖 Read Full Story →</a>',
            unsafe_allow_html=True
        )
        st.divider()

# Main dashboard
st.markdown('<h1 class="main-header">📰 TheIndianVisual News Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🔴 Live Indian News Monitoring | Auto-refreshes Every 2 Minutes</p>', unsafe_allow_html=True)

# Fetch news data
data_bundle = fetch_news()
news_data = data_bundle['news']
last_fetch_time = data_bundle['time']
st.session_state.news = news_data

# Update sidebar last update time
last_update_placeholder.markdown(f"---")
last_update_placeholder.caption(f"⏰ Last updated: {last_fetch_time}")

# Metrics row with enhanced styling
st.markdown('<div class="stats-section">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_count = len(news_data)
    st.markdown(f'''
    <div class="metric-card">
        <div style="font-size: 0.9rem; opacity: 0.9;">Total Stories</div>
        <div style="font-size: 2.5rem; font-weight: 700; margin-top: 0.5rem;">{total_count}</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    priority_count = len([n for n in news_data if n['priority'] == '🔴 PRIORITY'])
    st.markdown(f'''
    <div class="metric-card" style="background: linear-gradient(135deg, #FF4444 0%, #CC0000 100%);">
        <div style="font-size: 0.9rem; opacity: 0.9;">🔴 Priority</div>
        <div style="font-size: 2.5rem; font-weight: 700; margin-top: 0.5rem;">{priority_count}</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    trending_count = len([n for n in news_data if n['priority'] == '🟡 TRENDING'])
    st.markdown(f'''
    <div class="metric-card" style="background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);">
        <div style="font-size: 0.9rem; opacity: 0.9;">🟡 Trending</div>
        <div style="font-size: 2.5rem; font-weight: 700; margin-top: 0.5rem;">{trending_count}</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    sources_count = len(RSS_FEEDS)
    st.markdown(f'''
    <div class="metric-card">
        <div style="font-size: 0.9rem; opacity: 0.9;">📡 Sources</div>
        <div style="font-size: 2.5rem; font-weight: 700; margin-top: 0.5rem;">{sources_count}</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# News tabs with better organization
tab1, tab2, tab3, tab4 = st.tabs(["🔴 PRIORITY", "🟡 TRENDING", "📊 All News", "📈 Analytics"])

with tab1:
    st.subheader("🚨 Priority Stories (Social Issues, Justice, Students)")
    st.markdown("*Critical news about rape, assault, violence, protests, education, and law enforcement*")
    
    priority_news = [n for n in news_data if n['priority'] == '🔴 PRIORITY']
    
    if priority_news:
        for story in priority_news[:20]:
            display_news_card(story)
    else:
        st.info("No priority news at the moment.")

with tab2:
    st.subheader("📈 Trending Stories (Politics, Economy, Governance)")
    st.markdown("*Latest developments in politics, economy, infrastructure, and policies*")
    
    trending_news = [n for n in news_data if n['priority'] == '🟡 TRENDING']
    
    if trending_news:
        for story in trending_news[:20]:
            display_news_card(story)
    else:
        st.info("No trending news at the moment.")

with tab3:
    st.subheader("📚 All News Stories")
    st.markdown("*Complete view of all collected stories across all categories and sources*")
    
    # Search and filter in all news
    search_term = st.text_input("🔍 Search news", "")
    
    displayed_news = news_data
    if search_term:
        displayed_news = [n for n in news_data if search_term.lower() in (n['title'] + n['summary']).lower()]
    
    if displayed_news:
        for story in displayed_news[:30]:
            display_news_card(story)
    else:
        st.info("No news matching your search.")

with tab4:
    st.subheader("📊 News Analytics & Insights")
    
    if news_data:
        df = pd.DataFrame(news_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📰 Top News Sources")
            source_counts = df['source'].value_counts().head(10)
            st.bar_chart(source_counts)
        
        with col2:
            st.markdown("#### 🎯 Priority Breakdown")
            priority_counts = df['priority'].value_counts()
            fig = px.pie(values=priority_counts.values, names=priority_counts.index, title="Priority Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Additional stats
        col3, col4, col5 = st.columns(3)
        with col3:
            avg_summary_len = df['summary'].apply(len).mean()
            st.metric("Avg Summary Length", f"{int(avg_summary_len)} chars")
        
        with col4:
            stories_with_images = len(df[df['image'].notna()])
            st.metric("Stories with Images", f"{stories_with_images}/{len(df)}")
        
        with col5:
            unique_sources = df['source'].nunique()
            st.metric("Unique Sources", unique_sources)
        
        # Top authors
        st.markdown("#### ✍️ Top Contributors")
        if 'author' in df.columns:
            author_counts = df[df['author'] != 'Unknown']['author'].value_counts().head(5)
            if not author_counts.empty:
                st.bar_chart(author_counts)
            else:
                st.info("Author information not available for this batch of news.")
    else:
        st.warning("No data available for analytics.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1.5rem 0;">
    <p><strong>TheIndianVisual News Dashboard</strong> | Built with ❤️ using Streamlit</p>
    <p>📰 Aggregating news from 15+ Indian news sources | 🔄 Auto-refreshing data</p>
    <p style="font-size: 0.85rem;">Last fetched: {}</p>
</div>
""".format(last_fetch_time), unsafe_allow_html=True)
st.markdown("*TheIndianVisual News Dashboard | Built for instant news monitoring*")
