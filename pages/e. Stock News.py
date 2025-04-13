import streamlit as st
import requests

st.set_page_config(page_title="Stock News", page_icon="📰")

# Function to fetch news articles
def fetch_news(api_key, query):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'pageSize': 100,
        'apiKey': api_key,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get('articles', [])
    else:
        st.error('Error fetching news')
        return []

# Streamlit app
def main():
    st.title('Stock News Search App 📰')
    st.markdown(
    """###### This page allows users to search for the latest news related to specific stocks or companies. By entering a ticker symbol or company name, users can retrieve recent headlines and summaries from trusted news sources, helping them stay informed about market-moving events."""
)

    st.sidebar.header("Stock News search 👇")
    search = st.sidebar.text_input('Enter a keyword to search for news articles', "")

    # API Key (add your NewsAPI key here or use Streamlit secrets)
    api_key = st.secrets['NEWSAPI_KEY']

    # Button to trigger the search
    if search!='':
        if not api_key or api_key == 'your_api_key_here':
            st.error('Please provide a valid NewsAPI key')
        elif search!='':
            articles = fetch_news(api_key, search)
            if articles:
                for article in articles:
                    if article['title'] != '[Removed]' and article.get('urlToImage'):
                        st.subheader(article['title'])
                        if article.get('urlToImage'):
                            st.image(article['urlToImage'], width=600)
                        st.write(article['description'])
                        st.write(f"[Read more]({article['url']})")
            else:
                st.info('No articles found')

if __name__ == '__main__':
    main()
