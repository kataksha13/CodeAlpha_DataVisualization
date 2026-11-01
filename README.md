# CodeAlpha_DataVisualization

**CodeAlpha Data Analytics Internship, Task 3: Data Visualization**

Visual story built from the book dataset scraped in Task 1
([CodeAlpha_WebScraping](https://github.com/kataksha/CodeAlpha_WebScraping)):
1,000 books from Books to Scrape with price, star rating and stock status.

## Dashboard

![Dashboard](charts/00_dashboard.png)

## The story

> Replace this section with your own words after running the script and looking at the charts.
> Example structure:

1. **The catalogue:** how many books, what the average price is, how prices are spread.
2. **Ratings:** which star rating is most common.
3. **Price vs rating:** whether better-rated books cost more (look at charts 03, 04 and 06).
4. **Takeaway:** one sentence a business owner could act on.

## Charts

| File | What it shows |
|---|---|
| 00_dashboard.png | One-page summary with key numbers |
| 01_price_distribution.png | Histogram of prices with the average marked |
| 02_rating_distribution.png | Number of books per star rating |
| 03_avg_price_by_rating.png | Average price for each rating |
| 04_price_spread_by_rating.png | Boxplot of price within each rating |
| 05_price_bands.png | Number of books in each price band |
| 06_price_rating_heatmap.png | Price band vs rating counts |
| 07, 08 (optional) | Top categories and average price by category, created only if the dataset has a `category` column |

## Design choices

- One colour palette across all charts, with ratings shown from red (1 star) to green (5 stars)
- Descriptive titles, labelled axes and value labels on bars
- Price bands to make a continuous variable easier to read
- Gridlines kept light and unnecessary borders removed

## How to run

```bash
pip install -r requirements.txt
python visualize.py
```

The script reads `data/books_dataset.csv` and saves all charts in the `charts/` folder.

## Project structure

```
CodeAlpha_DataVisualization/
├── data/books_dataset.csv
├── charts/
├── visualize.py
├── requirements.txt
└── README.md
```

## Tools

Python, pandas, matplotlib, seaborn
