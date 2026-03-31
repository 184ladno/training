import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
conn = mysql.connector.connect(
    host="localhost",
    user="root",           
    password="Anastasiia184",   
    database="test_db"
)

query = """
    SELECT
        release_year,
        category,
        AVG(rating) AS avg_rating
    FROM apple_sales
    GROUP BY release_year, category
    ORDER BY release_year, category;
"""

df = pd.read_sql(query, conn)
conn.close()

print(df)
rating_pivot = df.pivot(index="release_year", columns="category", values="avg_rating")

years      = rating_pivot.index.astype(str).tolist()  
categories = rating_pivot.columns.tolist()

n_groups  = len(years)        
n_bars    = len(categories)
x         = np.arange(n_groups)
bar_width = 0.8 / n_bars    

palette = ["#007AFF", "#34C759", "#FF9500", "#FF2D55",
           "#AF52DE", "#5AC8FA", "#FFCC00", "#FF6B35", "#00C7BE"]
color_map = {cat: palette[i % len(palette)] for i, cat in enumerate(categories)}

fig, ax = plt.subplots(figsize=(16, 7), facecolor="#1C1C1E")
ax.set_facecolor("#2C2C2E")

for i, cat in enumerate(categories):
    offset = (i - n_bars / 2 + 0.5) * bar_width
    vals   = rating_pivot[cat].values
    bars   = ax.bar(
        x + offset, vals, bar_width - 0.02,
        label=cat,
        color=color_map[cat],
        edgecolor="#1C1C1E",
        linewidth=0.5
    )
    for bar, v in zip(bars, vals):
        if not np.isnan(v):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.03,
                f"{v:.1f}",
                ha="center", va="bottom",
                fontsize=7.5, color="white", fontweight="bold"
            )

ax.set_title("Apple Devices — Average Rating by Category & Year",
             fontsize=15, fontweight="bold", color="white", pad=15)
ax.set_xlabel("Release Year", color="white", fontsize=11)
ax.set_ylabel("Average Rating (out of 5)", color="white", fontsize=11)
ax.set_ylim(0, 5.8)
ax.set_xticks(x)
ax.set_xticklabels(years, color="white", fontsize=10)
ax.tick_params(axis="y", colors="white")
ax.grid(axis="y", color="#48484A", linestyle="--", linewidth=0.6, alpha=0.7)

for spine in ax.spines.values():
    spine.set_color("#48484A")

ax.legend(
    title="Category", title_fontsize=10,
    facecolor="#3A3A3C", labelcolor="white",
    framealpha=0.9, fontsize=9
)

plt.tight_layout()
plt.savefig("apple_rating_by_category.png", dpi=150,
            bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()
