"""Tasks 2-4: EDA, visualization and sentiment analysis."""
from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

DATA_DIR = Path("data")
OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

def load_reviews():
    # Prefer the user's real dataset if present; otherwise use clearly synthetic demo data.
    real_file = DATA_DIR / "reviews.csv"
    sample_file = DATA_DIR / "sample_reviews.csv"
    path = real_file if real_file.exists() else sample_file
    df = pd.read_csv(path)
    if "review" not in df.columns:
        raise ValueError("Your CSV must contain a column named 'review'.")
    print(f"Loaded {len(df)} rows from {path}")
    return df, path

def clean_data(df):
    df = df.copy()
    df["review"] = df["review"].fillna("").astype(str).str.strip()
    df = df[df["review"] != ""].drop_duplicates(subset=["review"])
    df["review_clean"] = df["review"].str.lower().apply(
        lambda value: re.sub(r"\s+", " ", value)
    )
    df["word_count"] = df["review_clean"].str.split().str.len()
    return df

def run_sentiment(df):
    try:
        nltk.data.find("sentiment/vader_lexicon.zip")
    except LookupError:
        nltk.download("vader_lexicon", quiet=True)
    analyzer = SentimentIntensityAnalyzer()
    scores = df["review"].apply(analyzer.polarity_scores)
    df["sentiment_score"] = scores.apply(lambda result: result["compound"])
    df["positive_score"] = scores.apply(lambda result: result["pos"])
    df["negative_score"] = scores.apply(lambda result: result["neg"])
    df["neutral_score"] = scores.apply(lambda result: result["neu"])
    df["sentiment"] = df["sentiment_score"].apply(
        lambda score: "Positive" if score >= 0.05
        else ("Negative" if score <= -0.05 else "Neutral")
    )
    return df

def create_outputs(df, source_path):
    # EDA summary
    summary = {
        "source_file": str(source_path),
        "rows_after_cleaning": len(df),
        "missing_reviews": int(df["review"].isna().sum()),
        "duplicate_reviews": int(df["review"].duplicated().sum()),
        "average_words_per_review": round(float(df["word_count"].mean()), 2) if len(df) else 0,
        "sentiment_counts": df["sentiment"].value_counts().to_dict()
    }
    pd.Series(summary, dtype="object").to_json(OUT_DIR / "eda_summary.json", indent=2)
    df.to_csv(OUT_DIR / "reviews_analyzed.csv", index=False, encoding="utf-8")

    sns.set_theme()
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x="sentiment", order=["Positive", "Neutral", "Negative"])
    plt.title("Review Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of reviews")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "sentiment_distribution.png", dpi=160)
    plt.close()

    plt.figure(figsize=(7, 5))
    sns.histplot(data=df, x="word_count", bins=10, kde=True)
    plt.title("Review Length Distribution")
    plt.xlabel("Number of words")
    plt.ylabel("Number of reviews")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "review_lengths.png", dpi=160)
    plt.close()

    if "rating" in df.columns and df["rating"].notna().any():
        plt.figure(figsize=(7, 5))
        sns.countplot(data=df, x="rating")
        plt.title("Rating Distribution")
        plt.xlabel("Rating")
        plt.ylabel("Number of reviews")
        plt.tight_layout()
        plt.savefig(OUT_DIR / "rating_distribution.png", dpi=160)
        plt.close()

    print("Analysis complete. Check the outputs/ folder.")
    print(df[["review", "sentiment", "sentiment_score"]].head(10).to_string(index=False))

if __name__ == "__main__":
    data, source = load_reviews()
    cleaned = clean_data(data)
    analyzed = run_sentiment(cleaned)
    create_outputs(analyzed, source)
