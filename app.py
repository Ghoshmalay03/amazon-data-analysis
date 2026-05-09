# import streamlit as st
# import pandas as pd

# # Load dataset
# df = pd.read_csv('data/amazon.csv')

# # Clean rating column
# df['rating'] = pd.to_numeric(
#     df['rating'],
#     errors='coerce'
# )

# # Title
# st.title("Amazon Product Data Analysis Dashboard")

# # Dataset preview
# st.subheader("Dataset Preview")
# st.dataframe(df.head())

# # Metrics
# st.metric(
#     "Average Rating",
#     round(df['rating'].mean(), 2)
# )

# st.metric(
#     "Total Products",
#     len(df)
# )

# # Category filter
# category = st.sidebar.selectbox(
#     "Select Category",
#     df['category'].unique()
# )

# filtered_df = df[
#     df['category'] == category
# ]

# st.subheader("Filtered Products")

# st.write(filtered_df.head())

# st.sidebar.title("Dashboard Filters")

# st.subheader("Rating Distribution")

# st.bar_chart(df['rating'].value_counts())

# df['actual_price'] = (
#     df['actual_price']
#     .str.replace('₹', '')
#     .str.replace(',', '')
#     .astype(float)
# )
# st.subheader("Product Prices")

# st.line_chart(df['actual_price'].head(50))

# st.metric(
#     "Average Price",
#     round(df['actual_price'].mean(), 2)
# )

# top_rated = df.sort_values(
#     by='rating',
#     ascending=False
# )

# st.subheader("Top Rated Products")

# st.write(
#     top_rated[
#         ['product_name', 'rating']
#     ].head(10)
# )

import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Amazon Product Analytics Dashboard",
    layout="wide"
)

# Load dataset
@st.cache_data

def load_data():
    df = pd.read_csv('data/amazon.csv')

    # Clean rating column
    df['rating'] = pd.to_numeric(
        df['rating'],
        errors='coerce'
    )

    # Clean actual price
    df['actual_price'] = (
        df['actual_price']
        .str.replace('₹', '')
        .str.replace(',', '')
        .astype(float)
    )

    # Clean discounted price
    df['discounted_price'] = (
        df['discounted_price']
        .str.replace('₹', '')
        .str.replace(',', '')
        .astype(float)
    )

    # Clean discount percentage
    df['discount_percentage'] = (
        df['discount_percentage']
        .str.replace('%', '')
        .astype(float)
    )

    # Clean rating count
    df['rating_count'] = (
        df['rating_count']
        .astype(str)
        .str.replace(',', '')
    )

    df['rating_count'] = pd.to_numeric(
        df['rating_count'],
        errors='coerce'
    )

    return df

# Load cleaned data

df = load_data()

# Dashboard title
st.title("Amazon Product Analytics Dashboard")

st.markdown("Interactive dashboard for Amazon product analysis using Python and Streamlit.")

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("Dashboard Filters")

# Search bar
search = st.sidebar.text_input("Search Product")

# Category filter
selected_category = st.sidebar.selectbox(
    "Select Category",
    options=['All'] + list(df['category'].dropna().unique())
)

# Rating filter
min_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)

# Price filter
max_price = st.sidebar.slider(
    "Maximum Price",
    min_value=0,
    max_value=int(df['actual_price'].max()),
    value=5000
)

# ---------------- FILTERING ---------------- #

filtered_df = df.copy()

if selected_category != 'All':
    filtered_df = filtered_df[
        filtered_df['category'] == selected_category
    ]

filtered_df = filtered_df[
    filtered_df['rating'] >= min_rating
]

filtered_df = filtered_df[
    filtered_df['actual_price'] <= max_price
]

if search:
    filtered_df = filtered_df[
        filtered_df['product_name']
        .str.contains(search, case=False, na=False)
    ]

# ---------------- METRICS ---------------- #

st.subheader("Dashboard Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Products",
        len(filtered_df)
    )

with col2:
    st.metric(
        "Average Rating",
        round(filtered_df['rating'].mean(), 2)
    )

with col3:
    st.metric(
        "Average Price",
        round(filtered_df['actual_price'].mean(), 2)
    )

with col4:
    st.metric(
        "Average Discount %",
        round(filtered_df['discount_percentage'].mean(), 2)
    )

# ---------------- DATA PREVIEW ---------------- #

st.subheader("Top Rated Products")

top_products = filtered_df.sort_values(
    by='rating',
    ascending=False
)

st.dataframe(
    top_products[
        [
            'product_name',
            'rating',
            'actual_price'
        ]
    ].head(10)
)

# ---------------- CHARTS ---------------- #

st.subheader("Price Distribution")

fig1 = px.histogram(
    filtered_df,
    x='actual_price',
    nbins=30,
    title='Product Price Distribution'
)

st.plotly_chart(fig1, use_container_width=True)

# Rating vs Price

st.subheader("Price vs Rating")

fig2 = px.scatter(
    filtered_df,
    x='actual_price',
    y='rating',
    color='rating',
    hover_data=['product_name'],
    title='Price vs Rating Analysis'
)

st.plotly_chart(fig2, use_container_width=True)

# Category Analysis

st.subheader("Top Categories")

category_count = (
    filtered_df['category']
    .value_counts()
    .head(10)
)

fig3 = px.bar(
    x=category_count.index,
    y=category_count.values,
    labels={'x': 'Category', 'y': 'Count'},
    title='Top Product Categories'
)

st.plotly_chart(fig3, use_container_width=True)

# Top Rated Products

st.subheader("Top Rated Products")

highest_rated = filtered_df.sort_values(
    by='rating',
    ascending=False
)

st.dataframe(
    highest_rated[
        [
            'product_name',
            'rating',
            'actual_price'
        ]
    ].head(10)
)

# ---------------- BUSINESS INSIGHTS ---------------- #

st.subheader("Business Insights")

st.markdown("""
1. Electronics dominate Amazon listings.
2. Most products maintain ratings above 4.
3. Mid-range products receive the highest reviews.
4. Heavy discounts do not always guarantee better ratings.
5. Highly reviewed products are generally moderately priced.
""")

# ---------------- FOOTER ---------------- #

st.markdown("---")
st.caption("Built using Python, Pandas, Streamlit, and Plotly")

if st.checkbox("Show Raw Dataset"):
    st.dataframe(df)