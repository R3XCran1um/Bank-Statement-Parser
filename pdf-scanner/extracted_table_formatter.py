import pandas as pd

def table_converter(tables):
    df_list = []
    # Convert each table to a DataFrame and add it to the list
    for i, table in enumerate(tables):
        df_list.append(table.df)
    return df_list

def table_combiner(df_list):
    combined_df = pd.concat(df_list, ignore_index=True)
    headers = combined_df.iloc[0].values
    combined_df.columns = headers
    combined_df.drop(index=0, axis=0, inplace=True)
    column_names = list(combined_df.columns)
    df_filtered = combined_df[~(combined_df == column_names).all(axis=1)]
    df_filtered.reset_index(drop=True, inplace=True)

    df_filtered.to_csv("extracted_transactions.csv", index=False)

    return df_filtered