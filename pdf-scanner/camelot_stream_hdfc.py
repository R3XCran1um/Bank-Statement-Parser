import camelot
import pandas as pd
import os
import numpy as np
from . import extracted_table_formatter, Infer_Statistics


def parse_pdf(file_name, password):
    print('hi')

    tables = camelot.read_pdf(
        file_name,
        pages="all",
        flavor="stream",
        table_areas=["0,610,650,60"],
        columns=["50,300,380,410,500,600"],
        password=password
    )

    df_list = extracted_table_formatter.table_converter(tables)
    df = extracted_table_formatter.table_combiner(df_list)
    
    df = df.drop(columns=["Chq./Ref.No.", "Value Dt"])

    df["Narration"] = df["Narration"].astype(str)

    df['Date'] = df['Date'].replace('', np.nan)
    df = df.dropna(subset=['Date'])

    df[["Withdrawal Amt.", "Deposit Amt."]] = df[
        ["Withdrawal Amt.", "Deposit Amt."]
    ].fillna(0)

    df.rename(
        columns={
            "Date": "TRANS DATE",
            "Deposit Amt.": "DEPOSIT",
            "Withdrawal Amt.": "WITHDRAWS",
            "Closing Balance": "BALANCE",
        },
        inplace=True,
    )

    df["TRANS DATE"] = pd.to_datetime(df["TRANS DATE"], format="%d/%m/%y")

    if df['TRANS DATE'].is_monotonic_decreasing:
        # Reindex to reverse the order
        df = df.reindex(index=df.index[::-1])
        
    df.to_csv("HDFC_statement_table.csv", index=False)

    statement_statistics = Infer_Statistics.Tabulate_statistics(df)
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'csv', 'hdfc_processed.csv')
    statement_statistics.to_csv(csv_path)
    print(f"CSV created at: {csv_path}")  # Replace with your actual variable that holds the path
