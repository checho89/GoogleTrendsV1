
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.dates import MonthLocator, YearLocator, DateFormatter

st.set_page_config(layout="wide")

st.title("📊 Google Trends – Time Series Exploration & Analysis")

DATA_DIR = "Google Trends Data Viz (start)"

files = {
    "Tesla vs Price": f"{DATA_DIR}/TESLA Search Trend vs Price.csv",
    "Unemployment": f"{DATA_DIR}/UE Benefits Search vs UE Rate 2004-20.csv",
    "Bitcoin Price (Daily)": f"{DATA_DIR}/Daily Bitcoin Price.csv",
    "Bitcoin Search (Monthly)": f"{DATA_DIR}/Bitcoin Search Trend.csv",
}


@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]

    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
    df = df.set_index(df.columns[0])

    return df


# ============================
# Dataset selection
# ============================
choice = st.selectbox("Choose dataset", list(files.keys()))
df = load_data(files[choice])

# ============================
# Data exploration section
# ============================
st.header("🔎 Data Exploration")

col1, col2 = st.columns(2)

with col1:
    st.write("### Shape")
    st.write(df.shape)

    st.write("### Columns")
    st.write(list(df.columns))

with col2:
    st.write("### Missing Values")
    st.write(df.isna().sum())

    if df.isna().sum().sum() > 0:
        st.write("Rows with NaNs")
        st.dataframe(df[df.isna().any(axis=1)])


st.write("### Descriptive Statistics")
st.dataframe(df.describe())


# ============================
# Periodicity detection
# ============================
st.header("⏱ Periodicity Detection")

diff = df.index.to_series().diff().dropna().value_counts().head(1)
st.write("Most common time difference:", diff.index[0])


# ============================
# Resampling
# ============================
st.header("🔁 Resampling")

freq = st.radio("Convert to:", ["Original", "Weekly", "Monthly"])

rule_map = {
    "Original": None,
    "Weekly": "W",
    "Monthly": "M"
}

if rule_map[freq]:
    df_plot = df.resample(rule_map[freq]).mean()
else:
    df_plot = df.copy()

st.write("Preview after resampling")
st.dataframe(df_plot.head())


# ============================
# Plot styling controls
# ============================
st.header("📈 Styled Time-Series Chart")

cols = st.multiselect(
    "Columns to plot",
    df_plot.columns.tolist(),
    default=df_plot.columns.tolist()[:2]
)

rolling_window = st.slider("Rolling average window", 1, 12, 1)

fig, ax = plt.subplots(figsize=(12, 6), dpi=160)

for col in cols:
    series = df_plot[col]

    ax.plot(
        series.index,
        series,
        linestyle='-',
        marker='o',
        linewidth=1.2,
        markersize=3,
        label=col
    )

    if rolling_window > 1:
        ax.plot(
            series.index,
            series.rolling(rolling_window).mean(),
            linestyle='--',
            linewidth=2,
            label=f"{col} (rolling)"
        )

ax.set_title(choice, fontsize=16)
ax.set_xlabel("Date")
ax.set_ylabel("Value")

ax.grid(True, which="both", linestyle="--", alpha=0.4)

# time axis locators
ax.xaxis.set_major_locator(YearLocator())
ax.xaxis.set_minor_locator(MonthLocator())
ax.xaxis.set_major_formatter(DateFormatter("%Y"))

plt.xticks(rotation=45)
plt.legend()

st.pyplot(fig)


# ============================
# Seasonality helper
# ============================
st.header("📅 Seasonality Helper (Monthly Mean)")

monthly = df.resample("M").mean()
season = monthly.groupby(monthly.index.month).mean()

st.dataframe(season)

st.success("✔ Exploration + resampling + styling + seasonality analysis ready.")
