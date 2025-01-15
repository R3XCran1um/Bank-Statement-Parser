import camelot
import pandas as pd
import numpy as np
import re
from . import extracted_table_formatter, Infer_Statistics

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
    file_name,
    pages="all",
    flavor="stream",
    table_areas=["0,610,650,60"],
    columns=["90,270,360,480"],
    password=password
    )

    df_list = extracted_table_formatter.table_converter(tables)
    df = extracted_table_formatter.table_combiner(df_list)

    df = df.drop(columns=["Chq/Ref No"])

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

    df["Balance"] = df["Balance"].str.replace(r"\(Cr\)|\(Dr\)", "", regex=True).str.replace(",", "").replace("", np.nan).astype(float)

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

    if df['TRANS DATE'].is_monotonic_decreasing:
        # Reindex to reverse the order
        df = df.reindex(index=df.index[::-1])

    df.to_csv("Kotak_statement_table.csv", index=False)

    statement_statistics = Infer_Statistics.Tabulate_statistics(df)
    statement_statistics.to_csv("Statement Statistics.csv")
