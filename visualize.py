"""
CodeAlpha Data Analytics Internship - Task 3: Data Visualization
Dataset: books_dataset.csv, scraped in Task 1 from books.toscrape.com

Usage:
    python visualize.py                          # uses data/books_dataset.csv
    python visualize.py --file path/to/file.csv

Creates individual charts and a one-page dashboard in the charts/ folder.
"""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save to files instead of opening windows
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

OUT_DIR = Path("charts")

# One consistent colour palette across all charts
BLUE, GREEN, ORANGE, RED, PURPLE = "#2E6F9E", "#3C9D6B", "#E08A2E", "#C0504D", "#7B5EA7"
RATING_COLORS = ["#C0504D", "#E08A2E", "#E3C34A", "#8FBF6B", "#3C9D6B"]  # 1 star (red) to 5 stars (green)

sns.set_theme(style="whitegrid", font_scale=1.0)
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path, dpi=140, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"saved {path}")


def add_price_band(df):
    bins = [0, 20, 30, 40, 50, 100]
    labels = ["Under £20", "£20-30", "£30-40", "£40-50", "£50+"]
    df["price_band"] = pd.cut(df["price_gbp"], bins=bins, labels=labels, right=False)
    return df


# ---------------------------------------------------------------------------
# Individual drawing functions. Each draws on a given axis so the same code
# builds both the single charts and the dashboard.
# ---------------------------------------------------------------------------
def draw_price_hist(ax, df):
    sns.histplot(df["price_gbp"], bins=25, color=BLUE, edgecolor="white", ax=ax)
    mean = df["price_gbp"].mean()
    ax.axvline(mean, color=RED, linestyle="--", linewidth=1.5)
    ax.text(mean + 0.7, ax.get_ylim()[1] * 0.92, f"Average £{mean:.2f}", color=RED, fontsize=9)
    ax.set_title("Distribution of book prices", loc="left", fontweight="bold")
    ax.set_xlabel("Price (£)")
    ax.set_ylabel("Number of books")


def draw_rating_bar(ax, df):
    counts = df["rating"].value_counts().reindex([1, 2, 3, 4, 5], fill_value=0)
    bars = ax.bar([str(i) for i in counts.index], counts.values, color=RATING_COLORS, edgecolor="white")
    for bar, v in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + counts.max() * 0.01, str(v), ha="center", fontsize=9)
    ax.set_title("How readers rate the books", loc="left", fontweight="bold")
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Number of books")


def draw_avg_price_by_rating(ax, df):
    avg = df.groupby("rating")["price_gbp"].mean().reindex([1, 2, 3, 4, 5])
    bars = ax.bar([str(i) for i in avg.index], avg.values, color=BLUE, edgecolor="white")
    for bar, v in zip(bars, avg.values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.3, f"£{v:.1f}", ha="center", fontsize=9)
    ax.set_title("Average price by star rating", loc="left", fontweight="bold")
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Average price (£)")


def draw_price_box(ax, df):
    sns.boxplot(data=df, x="rating", y="price_gbp", palette=RATING_COLORS, hue="rating",
                legend=False, ax=ax, linewidth=1)
    ax.set_title("Price spread within each rating", loc="left", fontweight="bold")
    ax.set_xlabel("Star rating")
    ax.set_ylabel("Price (£)")


def draw_price_bands(ax, df):
    counts = df["price_band"].value_counts().sort_index()
    ax.barh(counts.index.astype(str), counts.values, color=GREEN, edgecolor="white")
    for i, v in enumerate(counts.values):
        ax.text(v + counts.max() * 0.01, i, str(v), va="center", fontsize=9)
    ax.invert_yaxis()
    ax.set_title("Books by price band", loc="left", fontweight="bold")
    ax.set_xlabel("Number of books")
    ax.set_ylabel("")


def draw_heatmap(ax, df):
    table = pd.crosstab(df["price_band"], df["rating"])
    sns.heatmap(table, annot=True, fmt="d", cmap="Blues", cbar=False, linewidths=0.5, ax=ax)
    ax.set_title("Where books cluster: price band vs rating", loc="left", fontweight="bold")
    ax.set_xlabel("Star rating")
    ax.set_ylabel("")


def draw_top_categories(ax, df):
    top = df["category"].value_counts().head(10).sort_values()
    ax.barh(top.index, top.values, color=PURPLE, edgecolor="white")
    ax.set_title("Top 10 categories by number of books", loc="left", fontweight="bold")
    ax.set_xlabel("Number of books")
    ax.set_ylabel("")


def draw_category_price(ax, df):
    avg = (df.groupby("category")["price_gbp"].agg(["count", "mean"])
             .query("count >= 10")["mean"].sort_values().tail(10))
    ax.barh(avg.index, avg.values, color=ORANGE, edgecolor="white")
    ax.set_title("Most expensive categories (average price)", loc="left", fontweight="bold")
    ax.set_xlabel("Average price (£)")
    ax.set_ylabel("")


# ---------------------------------------------------------------------------
# Build outputs
# ---------------------------------------------------------------------------
def single_charts(df, has_category):
    charts = [
        ("01_price_distribution.png", draw_price_hist, (8, 5)),
        ("02_rating_distribution.png", draw_rating_bar, (7, 5)),
        ("03_avg_price_by_rating.png", draw_avg_price_by_rating, (7, 5)),
        ("04_price_spread_by_rating.png", draw_price_box, (8, 5)),
        ("05_price_bands.png", draw_price_bands, (8, 4.5)),
        ("06_price_rating_heatmap.png", draw_heatmap, (8, 5)),
    ]
    if has_category:
        charts += [
            ("07_top_categories.png", draw_top_categories, (9, 5.5)),
            ("08_category_avg_price.png", draw_category_price, (9, 5.5)),
        ]
    for name, func, size in charts:
        fig, ax = plt.subplots(figsize=size)
        func(ax, df)
        save(fig, name)


def dashboard(df, has_category):
    fig = plt.figure(figsize=(16, 11.5))
    fig.suptitle("Books to Scrape: Price and Rating Dashboard", fontsize=20, fontweight="bold", x=0.06, ha="left", y=0.985)

    # KPI strip
    kpis = [
        ("Books analysed", f"{len(df):,}"),
        ("Average price", f"£{df['price_gbp'].mean():.2f}"),
        ("Median price", f"£{df['price_gbp'].median():.2f}"),
        ("Average rating", f"{df['rating'].mean():.2f} / 5"),
        ("In stock", f"{df['in_stock'].mean() * 100:.0f}%"),
    ]
    for i, (label, value) in enumerate(kpis):
        x = 0.06 + i * 0.185
        fig.text(x, 0.922, value, fontsize=22, fontweight="bold", color=BLUE)
        fig.text(x, 0.902, label, fontsize=10, color="#555555")

    gs = fig.add_gridspec(2, 3, top=0.87, bottom=0.06, left=0.06, right=0.97, hspace=0.38, wspace=0.28)
    axes = [fig.add_subplot(gs[r, c]) for r in range(2) for c in range(3)]

    draw_price_hist(axes[0], df)
    draw_rating_bar(axes[1], df)
    draw_avg_price_by_rating(axes[2], df)
    draw_price_box(axes[3], df)
    draw_price_bands(axes[4], df)
    if has_category:
        draw_top_categories(axes[5], df)
    else:
        draw_heatmap(axes[5], df)

    save(fig, "00_dashboard.png")


def main():
    parser = argparse.ArgumentParser(description="Visualize the scraped books dataset")
    parser.add_argument("--file", default="data/books_dataset.csv", help="path to the CSV")
    args = parser.parse_args()

    csv_path = Path(args.file)
    if not csv_path.exists():
        print(f"Could not find {csv_path}. Put books_dataset.csv inside the 'data' folder.")
        return

    OUT_DIR.mkdir(exist_ok=True)
    df = add_price_band(pd.read_csv(csv_path))
    has_category = "category" in df.columns

    print(f"Loaded {len(df)} rows. Category data available: {has_category}\n")
    single_charts(df, has_category)
    dashboard(df, has_category)
    print("\nDone. Open the 'charts' folder to see your visuals.")


if __name__ == "__main__":
    main()
