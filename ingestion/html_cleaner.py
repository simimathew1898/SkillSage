# D:\SkillSage\ingestion\html_cleaner.py

import pandas as pd
from bs4 import BeautifulSoup
import os

def clean_html(raw_html):
    """
    Removes HTML tags from a string using BeautifulSoup.
    """
    if pd.isnull(raw_html):
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text(separator=" ")

# Load the raw job data
input_path = os.path.join("ingestion", "jobs_remoteok.csv")
df = pd.read_csv(input_path)

# Clean HTML from description column
df["description"] = df["description"].apply(clean_html)

# Save cleaned data
output_path = os.path.join("ingestion", "jobs_cleaned.csv")
df.to_csv(output_path, index=False)

print(f"HTML cleaned and saved to {output_path}")
