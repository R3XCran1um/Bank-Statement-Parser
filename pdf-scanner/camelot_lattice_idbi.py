import camelot
import pandas as pd
from . import extracted_table_formatter, Infer_Statistics

def parse_pdf(file_name, password):

    tables = camelot.read_pdf(
        file_name,
        pages="all",
        flavor="lattice",
        strip_text="\n",
        password=password
    )

    df_list = extracted_table_formatter.table_converter(tables)
    df = extracted_table_formatter.table_combiner(df_list)

    df = df.drop(columns=["Txn Date", "ChequeNo", "CCY"])

    df["Credit"] = df.apply(
        lambda row: row["Amount (INR)"] if row["CR/DR"] == "Cr." else 0.0, axis=1
    )
    df["Debit"] = df.apply(
        lambda row: row["Amount (INR)"] if row["CR/DR"] == "Dr." else 0.0, axis=1
    )
    df = df.drop(columns=["CR/DR", "Amount (INR)"])
    columns = list(df.columns)
    columns.remove("Balance (INR)")
    columns = columns + ["Balance (INR)"]
    df = df[columns]

    df.rename(columns={"Value Date": "TRANS DATE", "Credit": "DEPOSIT", "Debit": "WITHDRAWS", "Balance (INR)": "BALANCE"}, inplace=True)

    df["TRANS DATE"] = pd.to_datetime(df["TRANS DATE"], format="%d/%m/%Y")

    if df['TRANS DATE'].is_monotonic_decreasing:
        # Reindex to reverse the order
        df = df.reindex(index=df.index[::-1])

    df.to_csv("IDBI_statement_table.csv", index=False)

    statement_statistics = Infer_Statistics.Tabulate_statistics(df)
    statement_statistics.to_csv("Statement Statistics.csv")
