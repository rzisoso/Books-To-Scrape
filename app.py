# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go # Import for more advanced plotly features

# --- Page Configuration (set as first command) ---
st.set_page_config(
    page_title="Bookstore Market Intelligence Dashboard",
    page_icon="📚",
    layout="wide"  # "centered" or "wide"
)

# --- Data Loading ---
# Use @st.cache_data decorator to cache data and avoid reloading on every interaction
@st.cache_data
def load_data():
    df = pd.read_csv('books_data.csv')
    return df

df = load_data()

# --- Page Title ---
st.title("📚 Books-to-Scrape Market Intelligence Dashboard")
st.write("This is an interactive dashboard for analyzing book data from `books.toscrape.com`.")

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Price range slider
min_price = float(df['Price(£)'].min())
max_price = float(df['Price(£)'].max())
price_range = st.sidebar.slider(
    "Select Price Range (£)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price) # Default to the entire range
)

# Rating multiselect
# Ensure ratings are sorted numerically, from low to high
all_ratings = sorted(df['Rating'].unique())
selected_ratings = st.sidebar.multiselect(
    "Select Star Rating",
    options=all_ratings,
    default=all_ratings # Default to all selected
)

# --- Filter data based on selections ---
df_filtered = df[
    (df['Price(£)'] >= price_range[0]) &
    (df['Price(£)'] <= price_range[1]) &
    (df['Rating'].isin(selected_ratings))
]

# --- Main Page Content ---

# 1. Key Performance Indicators (KPIs)
st.header("Key Performance Indicators (KPIs)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Books (Filtered)", f"{len(df_filtered)}")
col2.metric("Average Price", f"£{df_filtered['Price(£)'].mean():.2f}")
col3.metric("Average Rating", f"{df_filtered['Rating'].mean():.2f} ⭐")


# 2. Data Visualization
st.header("Data Visualization")

# Price Distribution Histogram
fig_price = px.histogram(
    df_filtered,
    x='Price(£)',
    nbins=30, # Keep the bin count
    title='Distribution of Book Prices',
    color_discrete_sequence=px.colors.qualitative.Plotly # Use Plotly's default color sequence
)
# Add white borders to histogram bars for better visual separation
fig_price.update_traces(marker_line_width=1, marker_line_color='white') 
st.plotly_chart(fig_price, use_container_width=True)


# Star Rating Distribution Bar Chart
# Ensure ratings are sorted numerically, from low to high
rating_counts = df_filtered['Rating'].value_counts().sort_index().reset_index()
rating_counts.columns = ['Rating', 'Count of Books'] # Rename columns for Plotly

fig_rating = px.bar(
    rating_counts,
    x='Rating',
    y='Count of Books',
    title='Distribution of Book Ratings',
    labels={'Rating': 'Star Rating (⭐)', 'Count of Books': 'Number of Books'},
    color='Rating', # Color by star rating
    color_continuous_scale=px.colors.sequential.Viridis # Use continuous color scale
)
# Add white borders to bar chart bars for better visual separation
fig_rating.update_traces(marker_line_width=1, marker_line_color='white')
# Ensure X-axis is categorical and increase bar spacing
fig_rating.update_xaxes(type='category') 
fig_rating.update_layout(bargap=0.1) # Increase bar spacing

st.plotly_chart(fig_rating, use_container_width=True)


# 3. Raw Data Table
st.header("Browse Raw Data")
st.dataframe(df_filtered)