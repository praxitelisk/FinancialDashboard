import streamlit as st
import requests

st.set_page_config(page_title="Dataframe Profiling", page_icon="📰")

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
    st.title('News Search App')

    # Input field for the keyword
    keyword = st.text_input('Enter a keyword to search for news articles')

    # API Key (add your NewsAPI key here or use Streamlit secrets)
    api_key = st.secrets['NEWSAPI_KEY']

    # Button to trigger the search
    if st.button('Search'):
        if not api_key or api_key == 'your_api_key_here':
            st.error('Please provide a valid NewsAPI key')
        elif keyword:
            articles = fetch_news(api_key, keyword)
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
