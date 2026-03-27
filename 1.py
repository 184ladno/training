import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np

stocks = yf.download(["AAPL", "MSFT"], start="2020-01-01", end="2024-01-01")
close_prices = stocks["Close"]
returns = close_prices.pct_change()

profit = (close_prices.iloc[-1] / close_prices.iloc[0] - 1) * 100
volatility = returns.std() * 100

top_aapl = returns["AAPL"].nlargest(5)
top_msft = returns["MSFT"].nlargest(5)

table_data = {
    "AAPL Date":       top_aapl.index.strftime("%Y-%m-%d"),
    "AAPL Return (%)": (top_aapl.values * 100).round(2),
    "MSFT Date":       top_msft.index.strftime("%Y-%m-%d"),
    "MSFT Return (%)": (top_msft.values * 100).round(2),
}
df_table = pd.DataFrame(table_data)

fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1], hspace=0.4)

ax = fig.add_subplot(gs[0])
cum_returns = (1 + returns).cumprod()
cum_returns["AAPL"].plot(ax=ax, label="AAPL", color="#2196F3", linewidth=2)
cum_returns["MSFT"].plot(ax=ax, label="MSFT", color="#4CAF50", linewidth=2)

ax.set_title("Cumulative Returns: AAPL vs MSFT (2020–2024)", fontsize=14, fontweight="bold", pad=12)
ax.set_ylabel("Growth of $1 invested")
ax.set_xlabel("")
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.axhline(y=1, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

for ticker, color in [("AAPL", "#2196F3"), ("MSFT", "#4CAF50")]:
    final = cum_returns[ticker].iloc[-1]
    ax.annotate(
        f"{ticker}: +{(final - 1) * 100:.1f}%",
        xy=(cum_returns.index[-1], final),
        xytext=(-90, 8),
        textcoords="offset points",
        color=color,
        fontweight="bold",
        fontsize=10,
    )

ax2 = fig.add_subplot(gs[1])
ax2.axis("off")

col_labels = ["AAPL Date", "AAPL Return (%)", "MSFT Date", "MSFT Return (%)"]
cell_text = df_table.values.tolist()

table = ax2.table(
    cellText=cell_text,
    colLabels=col_labels,
    cellLoc="center",
    loc="center",
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.6)

for col in range(len(col_labels)):
    table[0, col].set_facecolor("#2C3E50")
    table[0, col].set_text_props(color="white", fontweight="bold")

for row in range(1, 6):
    table[row, 1].set_text_props(color="#1565C0", fontweight="bold")  
    table[row, 3].set_text_props(color="#2E7D32", fontweight="bold")  

    shade = "#F5F5F5" if row % 2 == 0 else "white"
    for col in range(4):
        table[row, col].set_facecolor(shade)

ax2.set_title("Top 5 Single-Day Gains (2020–2024)", fontsize=12, fontweight="bold", pad=8)

plt.suptitle("Stock Analysis Dashboard", fontsize=16, fontweight="bold", y=1.01)
plt.savefig("stock_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
