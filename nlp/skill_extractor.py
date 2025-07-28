import spacy
from spacy.matcher import PhraseMatcher
import pandas as pd
import os

# Load English NLP model
nlp = spacy.load("en_core_web_sm")

# Load job descriptions
df = pd.read_csv("ingestion/jobs_remoteok.csv")

# Load and clean skills list
skills_path = "nlp/skills_master_list.txt"
with open(skills_path, "r") as f:
    skills_list = [line.strip().lower() for line in f if line.strip()]

# Remove ambiguous/unreliable single-word skills
filtered_skills = [skill for skill in skills_list if len(skill) > 2 or ' ' in skill]

# Initialize matcher with lowercase attribute
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(skill) for skill in filtered_skills]
matcher.add("SKILLS", patterns)

# Dictionary to count skill occurrences
skill_counts = {}

# Iterate through job descriptions
for index, row in df.iterrows():
    description = str(row.get("description", "")).lower()
    doc = nlp(description)
    matches = matcher(doc)
    found_skills = set([doc[start:end].text.lower() for _, start, end in matches])
    
    for skill in found_skills:
        skill_counts[skill] = skill_counts.get(skill, 0) + 1

# Create a dataframe of top skills
skills_df = pd.DataFrame(skill_counts.items(), columns=["skill", "count"])
skills_df = skills_df.sort_values(by="count", ascending=False)

# Save to CSV
output_path = "data/processed/skills_ranked.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
skills_df.to_csv(output_path, index=False)

print(f"Skill extraction complete. Top {len(skills_df)} skills saved to {output_path}")
