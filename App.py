import requests
import streamlit as st

# ----------------- PAGE CONFIG -----------------
st.set_page_config(page_title="📰 News Reader App", layout="wide")

# ----------------- CUSTOM CSS -----------------
st.markdown("""
<style>
/* Main Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #E3FDFD, #CBF1F5, #A6E3E9, #71C9CE);
    color: #000000;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #1B262C, #0F4C75);
    color: #FFFFFF;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Sidebar headers */
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4 {
    color: #FFD369 !important;
}

/* Category Radio Buttons */
div[role="radiogroup"] > label {
    background-color: rgba(255, 255, 255, 0.1);
    color: #FFFFFF !important;
    border-radius: 8px;
    padding: 6px 10px;
    margin-bottom: 5px;
    display: block;
    cursor: pointer;
}
div[role="radiogroup"] > label:hover {
    background-color: #3282B8;
    color: #FFFFFF !important;
}

/* News Cards */
.news-card {
    background-color: #FFFFFF;
    padding: 15px;
    margin: 10px 0px;
    border-radius: 12px;
    box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
}
.news-card h4 {
    color: #0F4C75;
}
.news-card a {
    text-decoration: none;
    color: #3282B8;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ----------------- TITLE -----------------
st.markdown("<h1 style='text-align:center;'>Welcome to HeadlinesHub 📰, News Reader</h1>", unsafe_allow_html=True)
st.write("<p style='text-align:center; font-size:18px;'>Get the latest headlines by category or search for any topic.</p>", unsafe_allow_html=True)

# ----------------- API KEY -----------------
API_KEY = "246661c7ea0d4f5b9b7c0a277e5e57aa"   # Replace with your NewsAPI key
BASE_URL = "https://newsapi.org/v2/top-headlines"

# ----------------- CATEGORIES -----------------
categories = ["Technology", "Sports", "Business", "Entertainment", "Health", "Science"]

# Sidebar filters
st.sidebar.header("📂 News Categories")
selected_category = st.sidebar.radio("Select a category", categories)

# Search box
st.sidebar.header("🔍 Search News")
search_query = st.sidebar.text_input("Enter a topic")

# ----------------- FETCH NEWS FUNCTION -----------------
def fetch_news(category=None, query=None):
    params = {
        "apiKey": API_KEY,
        "language": "en",
        "pageSize": 8  # Limit to 8 articles for readability
    }
    if query:
        params["q"] = query
        url = "https://newsapi.org/v2/everything"
    else:
        params["category"] = category.lower()
        url = BASE_URL

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        st.error("⚠ Failed to fetch news. Check API key or quota.")
        return []

# ----------------- DISPLAY NEWS -----------------
if search_query:
    st.subheader(f"🔍 Search Results for: {search_query}")
    articles = fetch_news(query=search_query)
else:
    st.subheader(f"📂 Top {selected_category} News")
    articles = fetch_news(category=selected_category)

if articles:
    for article in articles:
        with st.container():
            st.markdown(
                f"""
                <div class="news-card">
                    <h4>{article['title']}</h4>
                    <p>{article.get('description', 'No description available.')}</p>
                    <a href="{article['url']}" target="_blank">Read more 🔗</a>
                </div>
                """,
                unsafe_allow_html=True
            )
else:
    st.info("No news found. Try another search or category.")

# ----------------- FOOTER -----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:16px;'>Made with ❤ by Vedant Vashishtha</p>", unsafe_allow_html=True)
