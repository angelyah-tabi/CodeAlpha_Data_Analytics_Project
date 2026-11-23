# CodeAlpha Data Analytics Internship Project

A beginner-friendly project demonstrating all four CodeAlpha Data Analytics tasks:
1. Web scraping
2. Exploratory Data Analysis (EDA)
3. Data visualization
4. Sentiment analysis

## Important note about the demo data
- The scraper uses `https://quotes.toscrape.com/`, a website made for scraping practice. It collects quotes, authors and tags.
- `data/sample_reviews.csv` contains clearly labelled **synthetic example reviews** so the sentiment-analysis workflow works immediately.
- For a real-world sentiment-analysis submission, replace the synthetic examples with a permitted public review dataset or reviews you have permission to use. Do not assume a website permits scraping; check its terms, robots.txt, rate limits and privacy rules first.

## 1. Install software
Install Python 3.10 or newer and VS Code (or use Jupyter Notebook).

Open a terminal in this project folder and run:

### Windows
```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 2. Run the scraper
```bash
python scraper.py
```
It creates `data/quotes_scraped.csv`.

## 3. Run EDA, charts and sentiment analysis
```bash
python analysis.py
```
It reads `data/sample_reviews.csv` and creates cleaned data, a text summary, charts and sentiment labels in `outputs/`.

To use your own dataset, save it as `data/reviews.csv` with a text column named `review`. Optionally include `rating` and `date` columns. The analysis script will prefer `reviews.csv` when it exists.

## 4. Launch the interactive dashboard
```bash
streamlit run app.py
```
A browser tab opens with dataset metrics, charts and sentiment results.

## Project structure
```text
codealpha_data_analytics_project/
├── app.py
├── scraper.py
├── analysis.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_reviews.csv
└── outputs/
```

## What to explain in your internship report
- Objective: understand text/review data using a reproducible analytics pipeline.
- Data collection: Requests downloads HTML; BeautifulSoup parses quote, author and tag elements.
- Data preparation: Pandas handles missing values and duplicate rows; text is normalized.
- EDA: inspect row counts, missing values, rating distribution (when available), text lengths and common words.
- Visualization: Matplotlib and Seaborn produce charts that make patterns easier to interpret.
- Sentiment: VADER returns positive, negative and neutral scores; a compound score is used to assign a label.
- Limitations: sentiment tools can misunderstand sarcasm, context, slang and mixed-language text. Validate results before drawing business conclusions.

## Suggested completion checklist
- [ ] Run the scraper and inspect the CSV.
- [ ] Run the analysis script and inspect all output files.
- [ ] Launch the Streamlit dashboard.
- [ ] Replace synthetic sample reviews with a permitted real dataset for a genuine case study.
- [ ] Write your own observations and conclusions.
- [ ] Upload source code and README to your GitHub repository.
- [ ] Record a short demo and submit it using the internship form.

Do not upload private information, passwords, API keys or data you do not have permission to share.
