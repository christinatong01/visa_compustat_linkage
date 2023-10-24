from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import pandas as pd
from google_matching import google_matching

visa = 'H-1B_visa_petitions_for_FY_2000.csv'
compustat = 'compustat_2000.csv'
output_csv = 'linkage_2000_goog.csv'
input_csv = 'H-1B_visa_petitions_for_FY_2000.csv'

visa_df = pd.read_csv(visa)
compustat_df = pd.read_csv(compustat)

results = []

def fuzzy_match_names(c1, c2):
    # print('\nSCORE', fuzz.partial_ratio(c1, c2))
    return fuzz.partial_ratio(c1, c2)

for index, row1 in visa_df.iterrows():
    name1 = row1['Employer Name']  
    output_row = ['', '', '']
    
    if pd.isna(name1):
        continue
    else:
        best_match, score, _ = process.extractOne(name1, compustat_df['conm'], scorer=fuzzy_match_names)
        if score >= 80:
            matched_row = compustat_df.loc[compustat_df['conm'] == best_match]
            gvkey = matched_row['gvkey'].values[0]
            output_row = [gvkey, best_match, score]
        else:
            google_match = google_matching(name1, compustat_df['conm'], compustat_df['weburl'], compustat_df['gvkey']) 
            if google_match is not None:
                output_row = [google_match[0], google_match[1], '']
    
    results.append(output_row)
    # print(output_row)
    

with open(input_csv, mode='r', newline='') as input_file:
    csv_reader = csv.reader(input_file)
    
    with open(output_csv, mode='w', newline='') as output_file:
        csv_writer = csv.writer(output_file, delimiter=',', escapechar='\\')
        
        for i, row in enumerate(csv_reader):
            if i == 0:
                output_row = row + ["gvkey", "best match", "score"]
                csv_writer.writerow(output_row)
            else:
                output_row = row + results[i]
                csv_writer.writerow(output_row)
