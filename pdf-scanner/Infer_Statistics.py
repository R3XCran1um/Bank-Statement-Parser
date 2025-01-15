import pandas as pd
import numpy as np
from datetime import datetime, date


def Tabulate_statistics(statement_table):
    df = statement_table.copy()
    df["TRANS DATE"] = pd.to_datetime(df["TRANS DATE"])
    # Add month and year columns for grouping
    df["Month"] = df["TRANS DATE"].dt.to_period("M")
    # processing_dates = [5, 10, 15, 20, 25]
    processing_dates = [1, 4, 5, 7, 10, 14, 15, 20, 21, 25, 28]
    df_with_processing_dates = pd.DataFrame()
    for x in processing_dates:
        mask = df["TRANS DATE"].dt.day > x
        greater_than_date_df = df[mask]

        # Find the smallest date greater than the 5th for each month
        smallest_dates = (
            greater_than_date_df.groupby("Month")["TRANS DATE"].min().reset_index()
        )
        smallest_dates_dict = smallest_dates.set_index("Month")["TRANS DATE"].to_dict()

        # Get the balance just before each smallest date
        result_list = []
        all_months = df["Month"].unique()

        """ for month in all_months:
            if month in smallest_dates_dict:
                min_date = smallest_dates_dict[month]
                # month_df = df[df["Month"] == month]
                before_min_date_df = df[df["TRANS DATE"] < min_date]
                if not before_min_date_df.empty:
                    last_balance = before_min_date_df.sort_values("TRANS DATE").iloc[-1][
                        "BALANCE"
                    ]
                    result_list.append((month.start_time.strftime("%m-%y"), last_balance))
                else:
                    result_list.append((month.start_time.strftime("%m-%y"), 0))
            else:
                # result_list.append((month.start_time.strftime("%m-%y"), 0))
                month_df = df[df["Month"] == month]
                if not month_df.empty:
                    last_balance = month_df.sort_values("TRANS DATE").iloc[-1]["BALANCE"]
                    result_list.append((month.start_time.strftime("%m-%y"), last_balance))
                else:
                    result_list.append((month.start_time.strftime("%m-%y"), None)) """

        for month in all_months:
            if month in smallest_dates_dict:
                min_date = smallest_dates_dict[month]
                before_min_date_df = df[df["TRANS DATE"] < min_date]
                
                if not before_min_date_df.empty:
                    # Get the last balance before the minimum date
                    last_balance = before_min_date_df.sort_values("TRANS DATE").iloc[-1]["BALANCE"]
                else:
                    last_balance = 0
                
                # Append the month and balance to the result list
                if isinstance(month, pd.Timestamp) or isinstance(month, pd.Period):
                    result_list.append((month.strftime("%m-%y"), last_balance))
                else:
                    result_list.append((month, last_balance))  # Assuming month is already in the desired format
            else:
                # Handle the case where month is not in the smallest_dates_dict
                month_df = df[df["Month"] == month]
                
                if not month_df.empty:
                    # Get the last balance for the current month
                    last_balance = month_df.sort_values("TRANS DATE").iloc[-1]["BALANCE"]
                else:
                    last_balance = None
                
                # Append the month and balance to the result list
                if isinstance(month, pd.Timestamp) or isinstance(month, pd.Period):
                    result_list.append((month.strftime("%m-%y"), last_balance))
                else:
                    result_list.append((month, last_balance))


        balances = [item[1] for item in result_list]
        df_with_processing_dates[str(x)] = balances

    month_year = [item[0] for item in result_list]
    df_with_processing_dates["Month-Year"] = month_year

    avg_index = df_with_processing_dates.columns.get_loc("Month-Year")

    for col in df_with_processing_dates.columns[:-1]:  #avg_index
        df_with_processing_dates[col] = df_with_processing_dates[col].replace(',', '', regex=True).astype(float)
    #print(df_with_processing_dates)

    #df_with_processing_dates['Average'] = df_with_processing_dates.iloc[:, 1:avg_index].mean(axis=1)
    #df_with_processing_dates.iloc[:, :-1] = df_with_processing_dates.iloc[:, :-1].apply(pd.to_numeric, errors='coerce')
    #print(type(df_with_processing_dates[0][0]))
    df_with_processing_dates["Average"] = df_with_processing_dates.iloc[:, :-1].mean(axis=1)

    df["Month-Year"] = df["TRANS DATE"].dt.strftime("%m-%y")
    df["DEPOSIT"] = df["DEPOSIT"].replace("", np.nan)
    df["DEPOSIT"] = df["DEPOSIT"].astype(str).str.replace(",", "").astype(float)
    df["WITHDRAWS"] = df["WITHDRAWS"].replace("", np.nan)
    df["WITHDRAWS"] = df["WITHDRAWS"].astype(str).str.replace(",", "").astype(float)
    non_zero_deposits = df[df["DEPOSIT"] > 0]
    non_zero_withdraws = df[df["WITHDRAWS"] > 0]

    # Group by Month-Year and calculate the total and number of deposits
    monthly_deposits = df.groupby("Month-Year")["DEPOSIT"].sum().reset_index()
    monthly_withdraws = df.groupby("Month-Year")["WITHDRAWS"].sum().reset_index()

    # Rename the columns for clarity
    monthly_deposits.columns = ["Month-Year", "Credit Total"]
    monthly_withdraws.columns = ["Month-Year", "Debit Total"]

    # Calculate the number of non-zero deposits per month
    credit_counts = (
        non_zero_deposits.groupby("Month-Year")
        .size()
        .reset_index(name="No. of Credits")
    )

    # Calculate the number of non-zero WITHDRAWSs per month
    debit_counts = (
        non_zero_withdraws.groupby("Month-Year")
        .size()
        .reset_index(name="No. of Debits")
    )

    # Merge the results with the first DataFrame
    result_df = pd.merge(df_with_processing_dates, monthly_deposits, on="Month-Year", how="left")
    result_df = pd.merge(result_df, monthly_withdraws, on="Month-Year", how="left")
    result_df = pd.merge(result_df, credit_counts, on="Month-Year", how="left")
    result_df = pd.merge(result_df, debit_counts, on="Month-Year", how="left")

    # current_time = datetime.now()
    # print(current_time.strftime('%Y-%m-%d'))

    current_date = date(2024, 9, 19)
    # Determine the starting year based on the current month
    start_year = current_date.year - 1

    # Define the starting month and year dynamically
    start_month = f"{start_year}-{current_date.month:02d}"

    # Generate a date range for 12 months starting from the current month of the previous year
    date_range = pd.date_range(start=start_month, periods=12, freq="MS")

    # Extract month and year in 'Month-YY' format
    months = date_range.strftime("%b-%y")

    # Create DataFrame and fill the column with the formatted month names
    summary = pd.DataFrame({"Month": months})

    result_df["Month-Year"] = pd.to_datetime(
        result_df["Month-Year"], format="%m-%y"
    ).dt.strftime("%b-%y")
    # Merge `summary` with `result_df` on the 'months' and 'Month-Year' columns
    final_df = pd.merge(
        summary, result_df, left_on="Month", right_on="Month-Year", how="left"
    )

    # Drop the extra 'Month-Year' column if no longer needed
    final_df.drop(columns=["Month-Year"], inplace=True)

    final_df.set_index("Month", inplace=True)

    cols_to_summarize = ["Average", "Credit Total", "Debit Total", "No. of Credits", "No. of Debits"]
    summary_row = {}
    grand_avg_index = final_df.columns.get_loc('Average')
    col_before_average = final_df.columns[grand_avg_index - 1]

    for col in final_df.columns:
        if col in cols_to_summarize:
            if col == 'Average':
                summary_row[col] = round((final_df[col].sum()) / 12, 2)
            else:
                summary_row[col] = final_df[col].sum()
        else:
            summary_row[col] = ""

    summary_row[col_before_average] = "Grand Average"

    summary_df = pd.DataFrame(summary_row, index=['Summary'])
    final_df = pd.concat([final_df, summary_df])

    return final_df
