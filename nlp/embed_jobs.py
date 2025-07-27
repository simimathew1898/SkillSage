from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
import os

# Load cleaned job descriptions
df = pd.read_csv("ingestion/jobs_cleaned.csv")
descriptions = df["description"].dropna().tolist()

# Load pretrained model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
embeddings = model.encode(descriptions, show_progress_bar=True)

# Save to file
output_path = "nlp/job_embeddings.npy"
np.save(output_path, embeddings)

print(f"Saved {len(embeddings)} embeddings to {output_path}")
