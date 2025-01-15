import tabula
import pandas as pd

pdf_path = "Shivam_Bank Statement _6 Months.pdf"
dfs = tabula.read_pdf(
    pdf_path,
    stream=True,
    pages="all",
    guess=True,
)
"""print(dfs[7])
print(dfs[7].shape)
print("required:", dfs[0].shape)"""

"""temp = dfs[7].iloc[:, :4]
print(temp)

print('\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n')
print(dfs[-1])
print(dfs[-1].shape)
print(dfs[-1].columns)


"""

processed_dfs = []
closing_bal = []
columns = []
for i, df in enumerate(dfs):
    if i == 0:
        # Keep the first dataframe as it is
        closing_bal.append(df.iloc[:, -1])
        df = df.iloc[:, [0, 1, 2, 3, -1]]
        columns = df.columns
        processed_dfs.append(df)
    else:
        df = df.iloc[:, [0, 1, 2, 3, -1]]
        # Create a new first row from the column headers
        new_first_row = pd.DataFrame([df.columns], columns=columns)
        # Align the columns to the first dataframe
        df.columns = columns
        # Concatenate the new header row and the dataframe
        df = pd.concat([new_first_row, df], ignore_index=True)
        closing_bal.append(df.iloc[:, -1])

        processed_dfs.append(df)

#cleaned_dfs = [df.dropna(axis=1, how='all') for df in processed_dfs]

print(processed_dfs[14])

"""for df, series in zip(processed_dfs, closing_bal):
    df['Closing Balance'] = series
"""

# Combine all processed dataframes
#combined_df = pd.concat(cleaned_dfs, ignore_index=True)


#combined_df.to_csv("extracted_transactions.csv", index=False)
