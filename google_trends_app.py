
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.dates import MonthLocator, YearLocator, DateFormatter

st.set_page_config(layout="wide")

st.title("📊 Google Trends – Cleaning, Resampling & Comparison Dashboard")

DATA_DIR = "Google Trends Data Viz (start)"

FILES = {
    "Tesla vs Price": (f"{DATA_DIR}/TESLA Search Trend vs Price.csv", "MONTH"),
    "Unemployment": (f"{DATA_DIR}/UE Benefits Search vs UE Rate 2004-20.csv", "MONTH"),
    "Bitcoin Search (Monthly)": (f"{DATA_DIR}/Bitcoin Search Trend.csv", "MONTH"),
    "Bitcoin Price (Daily)": (f"{DATA_DIR}/Daily Bitcoin Price.csv", "DATE"),
}


# -------------------------------------------------
# Cleaning + conversion function
# -------------------------------------------------
def clean_dataframe(path, date_col):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    df[date_col] = pd.to_datetime(df[date_col])

    nan_count = df.isna().sum().sum()

    nan_rows = df[df.isna().any(axis=1)] if nan_count > 0 else None

    df = df.dropna()

    df = df.set_index(date_col)

    return df, nan_count, nan_rows


# -------------------------------------------------
# Sidebar selection
# -------------------------------------------------
choice = st.sidebar.selectbox("Choose dataset", list(FILES.keys()))

path, date_col = FILES[choice]

df, nan_count, nan_rows = clean_dataframe(path, date_col)


# -------------------------------------------------
# Exploration
# -------------------------------------------------
st.header("🔎 Data Exploration")

c1, c2 = st.columns(2)

with c1:
    st.write("Shape:", df.shape)
    st.write("Columns:", list(df.columns))

with c2:
    st.write("Total NaNs removed:", nan_count)
    if nan_rows is not None:
        st.write("Rows with NaNs (before cleaning)")
        st.dataframe(nan_rows)


st.subheader("Descriptive Statistics")
st.dataframe(df.describe())


# -------------------------------------------------
# Periodicity detection
# -------------------------------------------------
st.header("⏱ Periodicity Detection")

diff = df.index.to_series().diff().dropna().value_counts().head(1)
st.write("Most common spacing:", diff.index[0])


# -------------------------------------------------
# Resampling
# -------------------------------------------------
st.header("🔁 Resampling")

freq = st.radio("Resample to:", ["Original", "Weekly", "Monthly"])

rule_map = {
    "Original": None,
    "Weekly": "W",
    "Monthly": "M"
}

if rule_map[freq]:
    df_plot = df.resample(rule_map[freq]).mean()
else:
    df_plot = df.copy()

st.dataframe(df_plot.head())


# -------------------------------------------------
# Plot
# -------------------------------------------------
st.header("📈 Styled Chart")

cols = st.multiselect(
    "Columns to plot",
    df_plot.columns.tolist(),
    default=df_plot.columns.tolist()[:2]
)

rolling = st.slider("Rolling average window", 1, 12, 1)

fig, ax = plt.subplots(figsize=(12, 6), dpi=160)

for col in cols:
    s = df_plot[col]

    ax.plot(s.index, s, marker="o", linestyle="-", linewidth=1.3, markersize=3, label=col)

    if rolling > 1:
        ax.plot(s.index, s.rolling(rolling).mean(), linestyle="--", linewidth=2, label=f"{col} rolling")

ax.set_title(choice)
ax.set_xlabel("Date")
ax.set_ylabel("Value")

ax.grid(True, linestyle="--", alpha=0.4)

ax.xaxis.set_major_locator(YearLocator())
ax.xaxis.set_minor_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter("%Y"))

plt.xticks(rotation=45)
plt.legend()

st.pyplot(fig)


# -------------------------------------------------
# Bitcoin comparison (special case)
# -------------------------------------------------
st.header("🪙 Bitcoin Price vs Search Comparison")

btc_price_path, _ = FILES["Bitcoin Price (Daily)"]
btc_search_path, _ = FILES["Bitcoin Search (Monthly)"]

btc_price, _, _ = clean_dataframe(btc_price_path, "DATE")
btc_search, _, _ = clean_dataframe(btc_search_path, "MONTH")

btc_monthly = btc_price.resample("M").last()

merged = btc_monthly.join(btc_search, how="inner")

st.write("Merged shape:", merged.shape)
st.dataframe(merged.head())

fig2, ax2 = plt.subplots(figsize=(12, 6), dpi=160)

ax2.plot(merged.index, merged.iloc[:, 0], linestyle="-", label="Price")
ax2.plot(merged.index, merged.iloc[:, -1], linestyle="--", label="Search")

ax2.grid(True, linestyle="--", alpha=0.4)
ax2.legend()
ax2.set_title("Bitcoin Monthly Price vs Search Popularity")

st.pyplot(fig2)

st.success("✔ Cleaning + NaN removal + datetime conversion + resampling + comparison implemented.")
