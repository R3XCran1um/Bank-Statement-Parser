import pandas as pd

# Read the CSV file
df = pd.read_csv('HDFC_statement_table.csv')

# Define the keywords to search for
keywords = ['ECS', 'ACH', 'EMI', 'CHQ RTN']

# Create an empty DataFrame to store the first occurrences
first_occurrences = pd.DataFrame()

# Loop through each keyword and find the first occurrence
for keyword in keywords:
    first_occurrence = df[df['Narration'].str.contains(keyword, na=False)].head(1)
    first_occurrences = pd.concat([first_occurrences, first_occurrence])

# Save the filtered DataFrame to a new CSV file
first_occurrences.to_csv('filtered_records.csv', index=False)
