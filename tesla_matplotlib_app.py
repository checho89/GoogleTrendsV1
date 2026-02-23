
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.dates as mdates

st.set_page_config(layout="wide")

st.title("🚗 Tesla Web Search vs Stock Price – Matplotlib Styling Demo")

DATA_PATH = "Google Trends Data Viz (start)/TESLA Search Trend vs Price.csv"


# -------------------------------------------------
# Load + clean
# -------------------------------------------------
@st.cache_data
def load_tesla():
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]

    df["MONTH"] = pd.to_datetime(df["MONTH"])

    # remove missing rows just in case
    df = df.dropna()

    return df


df_tesla = load_tesla()

st.subheader("Data Preview")
st.dataframe(df_tesla.head())


# -------------------------------------------------
# Chart controls
# -------------------------------------------------
st.sidebar.header("Chart Controls")

price_min = st.sidebar.number_input("Price min", 0, 2000, 0)
price_max = st.sidebar.number_input("Price max", 0, 2000, 600)

line_width = st.sidebar.slider("Line width", 1, 6, 3)
dpi_val = st.sidebar.slider("Resolution (DPI)", 80, 240, 120)


# -------------------------------------------------
# Styled Tesla chart (dual axis)
# -------------------------------------------------
st.header("📈 Styled Dual‑Axis Chart")

plt.figure(figsize=(14, 8), dpi=dpi_val)

plt.title("Tesla Web Search vs Price", fontsize=18)

# x tick styling
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

price_color = "#E6232E"   # red HEX
search_color = "skyblue" # named blue

ax1.set_ylabel("TSLA Stock Price (USD)", color=price_color, fontsize=14)
ax2.set_ylabel("Search Trend", color=search_color, fontsize=14)

# axis limits
ax1.set_ylim([price_min, price_max])
ax1.set_xlim([df_tesla.MONTH.min(), df_tesla.MONTH.max()])

# thicker lines
ax1.plot(
    df_tesla.MONTH,
    df_tesla.TSLA_USD_CLOSE,
    color=price_color,
    linewidth=line_width
)

ax2.plot(
    df_tesla.MONTH,
    df_tesla.TSLA_WEB_SEARCH,
    color=search_color,
    linewidth=line_width
)

# better time axis formatting
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

ax1.grid(True, linestyle="--", alpha=0.4)

plt.tight_layout()

st.pyplot(plt.gcf())

st.success("✔ Dual‑axis Tesla chart with full Matplotlib styling implemented.")
