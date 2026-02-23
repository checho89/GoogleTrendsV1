import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
file_path = "/mnt/data/UE Benefits Search vs UE Rate 2004-20.csv"
df = pd.read_csv(file_path)

# Convert MONTH column to datetime
df["MONTH"] = pd.to_datetime(df["MONTH"])

# Create figure
plt.figure(figsize=(14, 8), dpi=120)

# Create twin axes
ax1 = plt.gca()
ax2 = ax1.twinx()

# Labels
ax1.set_ylabel("Unemployment Rate (UNRATE)", fontsize=14)
ax2.set_ylabel("Search Trend (UE Benefits)", fontsize=14)

# X-axis range
ax1.set_xlim([df["MONTH"].min(), df["MONTH"].max()])

# Plot lines
ax1.plot(df["MONTH"], df["UNRATE"], linewidth=3)
ax2.plot(df["MONTH"], df["UE_BENEFITS_WEB_SEARCH"], linewidth=3)

# Title and ticks
plt.title('Monthly US "Unemployment Benefits" Search vs Unemployment Rate (incl. 2020)', fontsize=16)
plt.xticks(rotation=45)

plt.show()