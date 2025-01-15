import camelot
import pandas as pd
import numpy as np

# Read the PDF file
tables = camelot.read_pdf(
    "Axis Banking.pdf",
    pages="all",
    flavor="lattice",
    strip_text="\n",
    line_scale=40,
)

df_list = []
columns = []
# Convert each table to a DataFrame and add it to the list
for i, table in enumerate(tables):
    if i == 0:
        df_list.append(table.df)
        #columns = table.df.columns
    else:
        #if np.array_equal(table.df.iloc[0].values, columns):
            #table.df.drop(index=0, axis=0, inplace=True)
        df_list.append(table.df)


combined_df = pd.concat(df_list, ignore_index=True)
headers = combined_df.iloc[0].values
combined_df.columns = headers
combined_df.drop(index=0, axis=0, inplace=True)
column_names = list(combined_df.columns)
df_filtered = combined_df[~(combined_df == column_names).all(axis=1)]
df_filtered.reset_index(drop=True, inplace=True)

df_filtered.to_csv("extracted_transactions.csv", index=False)
