import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(layout="wide")

st.title("📱 Android App Store Analytics Dashboard")

DATA_PATH = "../GoogleTrends/GoogleAppStore/googleplaystore.csv"

# -----------------------------
# Load & clean data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    # remove duplicates
    df = df.drop_duplicates(subset="App")

    # clean installs
    df["Installs"] = (
        df["Installs"]
        .str.replace("+", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df["Installs"] = pd.to_numeric(df["Installs"], errors="coerce")

    # clean price
    df["Price"] = df["Price"].str.replace("$", "", regex=False)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    # rating numeric
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

    df = df.dropna(subset=["Installs", "Rating"])

    return df


df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())


# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()[:5]
)

type_filter = st.sidebar.multiselect(
    "App Type",
    df["Type"].dropna().unique(),
    default=df["Type"].dropna().unique()
)

filtered = df[
    (df["Category"].isin(category)) &
    (df["Type"].isin(type_filter))
]


# -----------------------------
# Category competition
# -----------------------------
st.header("🔥 Category Competition")

cat_count = (
    filtered.groupby("Category")
    .size()
    .reset_index(name="App Count")
    .sort_values("App Count", ascending=False)
)

fig1 = px.bar(
    cat_count,
    x="App Count",
    y="Category",
    orientation="h",
    title="Number of Apps per Category"
)

st.plotly_chart(fig1, use_container_width=True)


# -----------------------------
# Free vs Paid downloads
# -----------------------------
st.header("💰 Free vs Paid Downloads")

downloads = (
    filtered.groupby("Type")["Installs"]
    .mean()
    .reset_index()
)

fig2 = px.bar(
    downloads,
    x="Type",
    y="Installs",
    color="Type",
    title="Average Downloads Free vs Paid"
)

st.plotly_chart(fig2, use_container_width=True)


# -----------------------------
# Price vs rating
# -----------------------------
st.header("⭐ Price vs Rating")

fig3 = px.scatter(
    filtered,
    x="Price",
    y="Rating",
    color="Category",
    size="Installs",
    title="Price vs Rating vs Popularity"
)

st.plotly_chart(fig3, use_container_width=True)


# -----------------------------
# Market share donut
# -----------------------------
st.header("📊 Category Market Share")

market = (
    filtered.groupby("Category")["Installs"]
    .sum()
    .reset_index()
)

fig4 = px.pie(
    market,
    names="Category",
    values="Installs",
    hole=0.5,
    title="Install Market Share"
)

st.plotly_chart(fig4, use_container_width=True)


st.success("Dashboard ready — explore opportunities in the app market 🚀")