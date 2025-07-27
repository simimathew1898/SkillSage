# nlp/rank_skills.py

import pandas as pd
import re
from collections import Counter
import ast
import os

INPUT_PATH = "nlp/jobs_skills_raw.csv"
OUTPUT_PATH = "nlp/skills_ranked.csv"

def normalize_phrase(phrase):
    if not isinstance(phrase, str):
        return ""
    phrase = phrase.lower()
    phrase = re.sub(r'[^a-z0-9\s]', '', phrase)  # remove punctuation
    return phrase.strip()

def main():
    if not os.path.exists(INPUT_PATH):
        print(f"Input file not found: {INPUT_PATH}")
        return

    df = pd.read_csv(INPUT_PATH)

    if "skills" not in df.columns:
        print("Expected column 'skills' not found.")
        return

    all_skills = []

    for entry in df["skills"]:
        try:
            # Assumes skill list is stored as a stringified list
            parsed_skills = ast.literal_eval(entry)
            if isinstance(parsed_skills, list):
                for skill in parsed_skills:
                    cleaned = normalize_phrase(skill)
                    if cleaned:
                        all_skills.append(cleaned)
        except:
            continue

    # Count frequency
    skill_counts = Counter(all_skills)
    ranked_df = pd.DataFrame(skill_counts.items(), columns=["skill", "count"])
    ranked_df = ranked_df.sort_values(by="count", ascending=False)

    ranked_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved ranked skills to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
