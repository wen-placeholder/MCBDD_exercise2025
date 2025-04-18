from chembl_webresource_client.new_client import new_client
import pandas as pd
from tqdm import tqdm
import time

# Step 1: Retrieve all approved drugs
molecule = new_client.molecule
approved_drugs = molecule.filter(max_phase=4)

# Step 2: Filter for drugs with approval year and store relevant info
filtered = [
    {
        'molecule_chembl_id': drug['molecule_chembl_id'],
        'name': drug.get('pref_name'),
        'year': drug.get('first_approval')
    }
    for drug in approved_drugs
    if drug.get('first_approval') is not None
]

# Step 3: Sort drugs by year and name
sorted_drugs = sorted(filtered, key=lambda x: (x['year'], x['name'] or ""))

# Step 4: Filter for drugs approved since 2019
recent_drugs = [drug for drug in sorted_drugs if drug['year'] >= 2019]

# Step 5: For each drug, retrieve UniProt accession numbers of protein targets
mechanism = new_client.mechanism
target = new_client.target

results = []

for drug in tqdm(recent_drugs, desc="Retrieving UniProt targets"):
    chembl_id = drug['molecule_chembl_id']
    try:
        mechanisms = mechanism.filter(molecule_chembl_id=chembl_id)
        for mech in mechanisms:
            target_chembl_id = mech.get('target_chembl_id')
            if target_chembl_id:
                target_info = target.get(target_chembl_id)
                if 'target_components' in target_info:
                    for comp in target_info['target_components']:
                        for xref in comp.get('target_component_xrefs', []):
                            if xref['xref_src_db'] == 'UniProt':
                                results.append({
                                    'molecule_chembl_id': chembl_id,
                                    'drug_name': drug['name'],
                                    'approval_year': drug['year'],
                                    'target_chembl_id': target_chembl_id,
                                    'uniprot_id': xref['xref_id']
                                })
    except Exception as e:
        print(f"Error processing {chembl_id}: {e}")
    time.sleep(0.2)  # polite pause

# Convert results to DataFrame and save
df_targets = pd.DataFrame(results)
df_targets.to_csv("approved_drugs_uniprot_targets_since_2019.csv", index=False)
print("Saved to approved_drugs_uniprot_targets_since_2019.csv")
