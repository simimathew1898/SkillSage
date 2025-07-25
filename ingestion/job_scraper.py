# Import required libraries
import requests
import pandas as pd

# RemoteOK API endpoint
url = "https://remoteok.com/api"

# Headers to avoid being blocked 
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Step 1: Send a GET request to the API
response = requests.get(url, headers=headers)

# Step 2: Convert the JSON response to Python objects
jobs = response.json()[1:]

# Step 3: Create a list to store job data
data = []

# Step 4: Loop through jobs and extract relevant fields
for job in jobs:
    data.append({
        "title": job.get("position"),               # Job title
        "company": job.get("company"),              # Company name
        "location": job.get("location"),            # Job location
        "tags": ", ".join(job.get("tags", [])),     # Tags like 'Python', 'Remote'
        "description": job.get("description"),      # Full job description
        "url": job.get("url"),                      # Job posting link
    })

# Step 5: Convert the list to a DataFrame
df = pd.DataFrame(data)

# Step 6: Save the data to CSV file
df.to_csv("ingestion/jobs_remoteok.csv", index=False)

# Step 7: Print first 3 records to confirm
print("Job data saved to ingestion/jobs_remoteok.csv")
print(df.head(3))
