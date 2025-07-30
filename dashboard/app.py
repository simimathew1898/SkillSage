# dashboard/app.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="SkillSage Insights", layout="wide")

# ---------- LOAD DATA ----------
skills_df = pd.read_csv("data/processed/skills_ranked.csv")
jobs_df = pd.read_csv("data/processed/job_listings.csv")

# ---------- SIDEBAR CONTROLS ----------
st.sidebar.title("Filters")

# Job title filter
job_titles = sorted(jobs_df["title"].dropna().unique())
selected_title = st.sidebar.selectbox("Filter by Job Title", options=["All"] + job_titles)

# Top N filter
top_n = st.sidebar.slider("Top N to display", 5, 30, 15)

# Color palette
palette = st.sidebar.selectbox("Color Palette", options=["viridis", "magma", "plasma", "crest"])

# ---------- APPLY FILTER ----------
if selected_title != "All":
    jobs_filtered = jobs_df[jobs_df["title"] == selected_title]
else:
    jobs_filtered = jobs_df

# ---------- HEADER ----------
st.title("SkillSage: Job Market Skill Trends")

# Summary
st.markdown(f"**{len(jobs_filtered)}** jobs matched for **'{selected_title}'**")
st.markdown(f"Extracted **{len(skills_df)}** unique skill mentions from descriptions.")

# ---------- METRICS ----------
col1, col2, col3 = st.columns(3)
col1.metric("Total Jobs", len(jobs_df))
col2.metric("Filtered Jobs", len(jobs_filtered))
col3.metric("Top Skills Tracked", len(skills_df))

st.markdown("---")

# ---------- LAYOUT ----------
left_col, right_col = st.columns(2)

# Top Skills Chart
with left_col:
    st.subheader(f"Top {top_n} Skills from Listings")
    fig1, ax1 = plt.subplots()
    sns.barplot(data=skills_df.head(top_n), x="count", y="skill", palette=palette, ax=ax1)
    ax1.set_xlabel("Mentions")
    ax1.set_ylabel("Skill")
    st.pyplot(fig1)

# Top Companies Chart
with right_col:
    st.subheader("Top Hiring Companies")
    top_companies = jobs_filtered["company"].value_counts().head(top_n)
    fig2, ax2 = plt.subplots()
    sns.barplot(x=top_companies.values, y=top_companies.index, palette=palette, ax=ax2)
    ax2.set_xlabel("Job Listings")
    ax2.set_ylabel("Company")
    st.pyplot(fig2)

st.markdown("---")

# ---------- OPTIONAL: Sample Listings ----------
st.subheader("📝 Sample Job Listings")
st.dataframe(jobs_filtered[["title", "company", "location"]].head(10), use_container_width=True)
