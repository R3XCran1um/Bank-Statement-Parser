import camelot
import pandas as pd
from . import extracted_table_formatter, Infer_Statistics

def parse_pdf(file_name, password):

    tables = camelot.read_pdf(
        file_name,
        pages="all",
        flavor="lattice",
        #backend="poppler",
        strip_text="\n",
        line_scale=40,
        password=password
    )

    df_list = extracted_table_formatter.table_converter(tables)
    df = extracted_table_formatter.table_combiner(df_list)

    df = df.drop(columns=["Chq No", "Init.Br"])

    df['Credit'].replace('', 0.0, inplace=True)
    df['Debit'].replace('', 0.0, inplace=True)

    df.rename(
        columns={
            "Tran Date": "TRANS DATE",
            "Credit": "DEPOSIT",
            "Debit": "WITHDRAWS",
            "Balance": "BALANCE",
        },
        inplace=True,
    )

    df["TRANS DATE"] = pd.to_datetime(df["TRANS DATE"], format="%d-%m-%Y")
    df.dropna(subset=["TRANS DATE"], inplace=True)

    if df['TRANS DATE'].is_monotonic_decreasing:
        # Reindex to reverse the order
        df = df.reindex(index=df.index[::-1])

    df.to_csv("Axis_statement_table.csv", index=False)

    statement_statistics = Infer_Statistics.Tabulate_statistics(df)
    statement_statistics.to_csv("Statement Statistics.csv")
