"""Optional interactive Streamlit dashboard."""
from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="CodeAlpha Data Analytics", page_icon="📊", layout="wide")
st.title("📊 CodeAlpha Data Analytics Dashboard")
st.caption("EDA • Data Visualization • Sentiment Analysis")

result_file = Path("outputs/reviews_analyzed.csv")
if not result_file.exists():
    st.warning("Run `python analysis.py` first to generate the analyzed dataset.")
    st.stop()

df = pd.read_csv(result_file)
total = len(df)
positive = int((df["sentiment"] == "Positive").sum())
negative = int((df["sentiment"] == "Negative").sum())
neutral = int((df["sentiment"] == "Neutral").sum())

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total reviews", total)
c2.metric("Positive", positive)
c3.metric("Negative", negative)
c4.metric("Neutral", neutral)

st.subheader("Sentiment distribution")
counts = df["sentiment"].value_counts().reindex(["Positive", "Neutral", "Negative"], fill_value=0)
fig, ax = plt.subplots()
counts.plot(kind="bar", ax=ax)
ax.set_xlabel("Sentiment")
ax.set_ylabel("Number of reviews")
st.pyplot(fig)

st.subheader("Explore reviews")
choice = st.selectbox("Filter by sentiment", ["All", "Positive", "Neutral", "Negative"])
filtered = df if choice == "All" else df[df["sentiment"] == choice]
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download analyzed CSV",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="reviews_analyzed.csv",
    mime="text/csv"
)
