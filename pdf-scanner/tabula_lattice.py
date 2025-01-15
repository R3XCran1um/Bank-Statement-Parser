import tabula
import pandas as pd

pdf_path = "IDBI Banking.pdf"
dfs = tabula.read_pdf(
    pdf_path,
    stream=False,
    pages="all",
    guess=True,
)

print(dfs[1])

processed_dfs = []
closing_bal = []
columns = []
for i, df in enumerate(dfs):
    print(i)
    if i == 0:
        # Keep the first dataframe as it is
        columns = df.columns
        processed_dfs.append(df)
    else:
        # Create a new first row from the column headers
        new_first_row = pd.DataFrame([df.columns], columns=columns)
        # Align the columns to the first dataframe
        df.columns = columns
        # Concatenate the new header row and the dataframe
        df = pd.concat([new_first_row, df], ignore_index=True)
        processed_dfs.append(df)

# cleaned_dfs = [df.dropna(axis=1, how='all') for df in processed_dfs]

#print(processed_dfs[14])

"""for df, series in zip(processed_dfs, closing_bal):
    df['Closing Balance'] = series
"""

# Combine all processed dataframes
combined_df = pd.concat(processed_dfs, ignore_index=True)
combined_df.to_csv("extracted_transactions.csv", index=False)
