import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="SkillSage Analytics",
    layout="wide"
)

# -------------------------------
# Load Data with Caching
# -------------------------------
@st.cache_data
def load_data():
    file_path = "data/processed/skills_ranked.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df.sort_values(by="count", ascending=False).reset_index(drop=True)
    else:
        return pd.DataFrame()

df = load_data()

# -------------------------------
# Title & Description
# -------------------------------
st.title("SkillSage – In-Demand Skills Dashboard")
st.markdown("""
SkillSage dashboard!  
""")

# -------------------------------
# UI Controls
# -------------------------------
with st.sidebar:
    st.header("Customize View")
    show_data = st.checkbox("Show Raw Data", value=False)
    top_n = st.slider("Top N Skills to Display", min_value=5, max_value=50, value=20)
    color_palette = st.selectbox("Color Palette", options=["viridis", "Blues", "magma", "rocket"])

# -------------------------------
# Show Raw Data (Optional)
# -------------------------------
if show_data:
    st.subheader("Raw Skill Frequency Data")
    st.dataframe(df)

# -------------------------------
# Plot Section
# -------------------------------
if not df.empty:
    st.subheader(f"Top {top_n} In-Demand Skills")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=df.head(top_n), x="count", y="skill", palette=color_palette, ax=ax)
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Skill")
    st.pyplot(fig)
else:
    st.warning("Skill data not found. Please make sure the file exists at 'data/processed/skills_ranked.csv'.")
