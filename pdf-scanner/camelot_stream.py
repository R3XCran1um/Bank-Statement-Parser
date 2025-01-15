import camelot
import pandas as pd
import numpy as np
import re
from Infer_Statistics import Tabulate_statistics

def extract_amount_type(value):
    if pd.isna(value):
        return None, None
    value = str(value).replace(",", "")
    match = re.match(r"(\d+\.\d{2})\((Dr|Cr)\)", str(value))
    if match:
        amount = float(match.group(1))
        trans_type = match.group(2)
        return amount, trans_type
    return None, None

def parse_pdf(file_name, password):

    tables = camelot.read_pdf(
        "Statements/Divyang_Bnking.PDF",
        pages="all",
        flavor="stream",
        # strip_text="\n",
        # row_tol=100
        table_areas=["0,610,650,60"],
        columns=["90,270,360,480"],  # for Kotak
        password=password
    )

    df_list = []
    # Convert each table to a DataFrame and add it to the list
    for i, table in enumerate(tables):
        if i == 0:
            df_list.append(table.df)
        else:
            df_list.append(table.df)


    combined_df = pd.concat(df_list, ignore_index=True)
    headers = combined_df.iloc[0].values
    combined_df.columns = headers
    combined_df.drop(index=0, axis=0, inplace=True)
    column_names = list(combined_df.columns)
    df_filtered = combined_df[~(combined_df == column_names).all(axis=1)]
    df_filtered.reset_index(drop=True, inplace=True)

    df_filtered.to_csv("extracted_transactions.csv", index=False)

    df = df_filtered.drop(columns=["Chq/Ref No"])

    df['Date'] = df['Date'].replace('', np.nan)
    df = df.dropna(subset=['Date'])

    df["Amount"], df["Type"] = zip(*df["Withdrawal (Dr)/"].apply(extract_amount_type))

    df["Credit"] = 0.0
    df["Debit"] = 0.0

    df.loc[df["Type"] == "Cr", "Credit"] = df["Amount"]
    df.loc[df["Type"] == "Dr", "Debit"] = df["Amount"]

    df["Credit"] = df["Credit"].astype(float)
    df["Debit"] = df["Debit"].astype(float)

    df = df.drop(columns=["Amount", "Type", "Withdrawal (Dr)/"])

    columns = list(df.columns)
    columns.remove("Balance")
    columns = columns + ["Balance"]
    df = df[columns]

    df["Balance"] = df["Balance"].str.replace(r"\(Cr\)", "", regex=True)

    df.rename(
        columns={
            "Date": "TRANS DATE",
            "Credit": "DEPOSIT",
            "Debit": "WITHDRAWS",
            "Balance": "BALANCE",
        },
        inplace=True,
    )

    df["TRANS DATE"] = pd.to_datetime(df["TRANS DATE"], format="%d-%m-%Y", errors="coerce")
    df = df[df["TRANS DATE"].notna()]

    df.to_csv("Kotak_statement_table.csv", index=False)

    statement_statistics = Tabulate_statistics(df)
    statement_statistics.to_csv("Statement Statistics.csv")