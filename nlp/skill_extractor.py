# D:\SkillSage\ingestion\skill_extractor.py

import pandas as pd
import spacy
import os

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load the cleaned job descriptions
input_path = os.path.join("ingestion", "jobs_cleaned.csv")
df = pd.read_csv(input_path)

# Function to extract noun chunks from description
def extract_skills(text):
    if pd.isnull(text):
        return []
    doc = nlp(text)
    # Only keep chunks that are 1-4 words and don’t start with stopwords
    skills = [chunk.text.strip().lower()
              for chunk in doc.noun_chunks
              if 1 <= len(chunk.text.split()) <= 4 and not chunk.root.is_stop]
    return list(set(skills))  # remove duplicates

# Apply the skill extraction
df["extracted_skills"] = df["description"].apply(extract_skills)

# Save output
output_path = os.path.join("nlp", "jobs_skills_raw.csv")
df.to_csv(output_path, index=False)

print(f"Skill-like phrases extracted and saved to {output_path}")
