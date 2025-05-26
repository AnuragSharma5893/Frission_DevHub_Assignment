import streamlit as st
import pandas as pd
from main import scrape_google_maps

st.set_page_config(page_title="Google Maps Scraper", layout="centered")

st.title("📍 Google Maps Restaurant Scraper")
st.markdown("Scrape restaurant data (name, address, phone) from Google Maps.")

query = st.text_input("Enter your search query (e.g., restaurants in Delhi):")
limit = st.slider("How many places to scrape?", 5, 50, 10)

if st.button("Start Scraping"):
    with st.spinner("Scraping in progress..."):
        try:
            df = scrape_google_maps(query, limit)
            st.success("Scraping completed successfully!")
            st.dataframe(df)
            st.download_button("Download CSV", df.to_csv(index=False), "output.csv", "text/csv")
        except Exception as e:
            st.error(f"An error occurred: {e}")
