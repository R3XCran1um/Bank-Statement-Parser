import camelot
import numpy as np
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

    df = df.drop(columns=["VALUE DATE", "BRANCH", "REF/CHQ.NO", ])

    df['TRANS DATE'] = df['TRANS DATE'].replace('', np.nan)
    df = df.dropna(subset=['TRANS DATE'])

    df["TRANS DATE"] = pd.to_datetime(df["TRANS DATE"], format="%d-%b-%y", errors="coerce")
    df = df.dropna(subset=["TRANS DATE"])

    if df['TRANS DATE'].is_monotonic_decreasing:
        # Reindex to reverse the order
        df = df.reindex(index=df.index[::-1])

    df.to_csv("Canara_statement_table.csv", index=False)

    statement_statistics = Infer_Statistics.Tabulate_statistics(df)
    #print(statement_statistics)
    statement_statistics.to_csv("Statement Statistics.csv")