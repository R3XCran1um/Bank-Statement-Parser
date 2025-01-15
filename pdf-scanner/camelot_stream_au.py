import camelot
import pandas as pd
import numpy as np
from . import extracted_table_formatter, Infer_Statistics

def parse_pdf(file_name, password):

    tables = camelot.read_pdf(
        file_name,
        pages="1",
        flavor="stream",
        table_areas=["0, 800, 1200, 150"],
        row_tol=10,
        password=password
    )

    list_1 = extracted_table_formatter.table_converter(tables)

    tables = camelot.read_pdf(
        file_name,
        pages="2-end",
        flavor="stream",
        table_areas=["0, 1100, 1200, 150"],
        columns=["130, 450, 580, 800, 980, 1100"],
        row_tol=10,
        password=password
    )

    list_2 = extracted_table_formatter.table_converter(tables)
    df_list = list_1 + list_2

    df = extracted_table_formatter.table_combiner(df_list)

    df = df.drop(columns=["Value date", "Chq./Ref. No."])

    rows_to_delete = []

    for i in range(1, len(df)):
        if pd.isna(df.at[i, "Date"]) or df.at[i, "Date"] == "":
            df.at[i - 1, "Description/Narration"] = (
                str(df.at[i - 1, "Description/Narration"])
                + " "
                + str(df.at[i, "Description/Narration"])
            )
            rows_to_delete.append(i)

    # Delete the rows where date was empty
    df = df.drop(rows_to_delete).reset_index(drop=True)

    df.rename(
        columns={
            "Date": "TRANS DATE",
            "Credit(Cr.)": "DEPOSIT",
            "Debit(Dr.)": "WITHDRAWS",
            "Balance": "BALANCE",
        },
        inplace=True,
    )

    df["WITHDRAWS"] = df["WITHDRAWS"].replace("-", 0).astype(float)
    df["DEPOSIT"] = df["DEPOSIT"].replace("-", 0).astype(float)

    df["TRANS DATE"] = pd.to_datetime(df["TRANS DATE"], format="%d %b %Y")
    df.dropna(subset=["TRANS DATE"], inplace=True)

    if df['TRANS DATE'].is_monotonic_decreasing:
        # Reindex to reverse the order
        df = df.reindex(index=df.index[::-1])

    df.to_csv("AU_statement_table.csv", index=False)

    statement_statistics = Infer_Statistics.Tabulate_statistics(df)
    statement_statistics.to_csv("Statement Statistics.csv")
