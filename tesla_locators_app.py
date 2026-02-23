
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.dates as mdates

st.set_page_config(layout="wide")

st.title("📅 Tesla Timeline with Locators & DateFormatters")

DATA_PATH = "Google Trends Data Viz (start)/TESLA Search Trend vs Price.csv"


# -----------------------------
# Load + clean
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]
    df["MONTH"] = pd.to_datetime(df["MONTH"])
    df = df.dropna()
    return df


df = load_data()

st.subheader("Preview")
st.dataframe(df.head())


# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Chart Options")

dpi_val = st.sidebar.slider("DPI", 80, 240, 120)
linewidth = st.sidebar.slider("Line width", 1, 6, 3)


# -----------------------------
# Matplotlib styling with locators
# -----------------------------
st.header("📈 Dual Axis Chart with Custom Tick Marks")

plt.figure(figsize=(14, 8), dpi=dpi_val)

ax1 = plt.gca()
ax2 = ax1.twinx()

price_color = "#E6232E"
search_color = "skyblue"

# ----- Locators & formatters -----
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter("%Y")

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

# ----- Labels -----
ax1.set_title("Tesla Web Search vs Price", fontsize=18)
ax1.set_ylabel("Stock Price (USD)", color=price_color, fontsize=14)
ax2.set_ylabel("Search Trend", color=search_color, fontsize=14)

plt.xticks(rotation=45, fontsize=14)

# ----- Limits -----
ax1.set_xlim(df.MONTH.min(), df.MONTH.max())
ax1.set_ylim(0, df.TSLA_USD_CLOSE.max() * 1.1)

# ----- Lines -----
ax1.plot(df.MONTH, df.TSLA_USD_CLOSE, color=price_color, linewidth=linewidth)
ax2.plot(df.MONTH, df.TSLA_WEB_SEARCH, color=search_color, linewidth=linewidth)

ax1.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

st.pyplot(plt.gcf())

st.success("✔ Major ticks = years | Minor ticks = months using Matplotlib locators.")
