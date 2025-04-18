import requests
import pandas as pd
import time

df_targets = pd.read_csv("approved_drugs_uniprot_targets_since_2019.csv")

# Get a list of unique UniProt IDs
uniprot_ids = df_targets['uniprot_id'].dropna().unique()

# Function to fetch keywords for one UniProt ID
def get_uniprot_keywords(uniprot_id):
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.ok:
            data = response.json()
            keywords = data['keywords']
            print(f"Keywords for {uniprot_id}")
            return keywords
    except Exception as e:
        print(f"Failed for {uniprot_id}: {e}")
    return []

# Retrieve keywords
records = []
for uid in uniprot_ids:
    keywords = get_uniprot_keywords(uid)
    for kw in keywords:
        records.append({'uniprot_id': uid, 'keyword': kw})
    time.sleep(0.5)  # Be polite to the API

# Convert to DataFrame
df_keywords = pd.DataFrame(records)

# Optionally merge with your original targets
df_merged = df_targets.merge(df_keywords, on='uniprot_id', how='left')

# Save results
df_merged.to_csv("approved_drugs_uniprot_keywords_since_2019.csv", index=False)
print("Saved UniProt keyword data to approved_drugs_uniprot_keywords_since_2019.csv")
