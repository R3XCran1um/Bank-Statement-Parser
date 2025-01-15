import pdfplumber
import pandas as pd


def replace_newlines(item):
    if isinstance(item, list):
        return [replace_newlines(sub_item) for sub_item in item]
    elif isinstance(item, str):
        return item.replace("\n", "")
    else:
        return item


pdf_path = "Shivam_Bank Statement _6 Months.pdf"

with pdfplumber.open(pdf_path) as pdf:
    print('hello')
    data = []
    # Iterate through pages
    for page in pdf.pages:
        tables = page.extract_tables()

        for row in tables:
            # print(row)
            data.append(row)

    columns = [item.replace("\n", " ") for item in data[0][0]]

    print(data)
'''
    for sublist in data:
        for i in range(len(sublist)):
            if sublist[i] == data[0][0]:
                sublist[i] = None  

    
    for sublist in data:
        sublist[:] = [x for x in sublist if x is not None]

    data = [[x for x in sublist if x] for sublist in data]

    clean_data = replace_newlines(data)
    #filtered_data = [row for row in clean_data if len(row) == len(columns)]
    flattened_list = [
        sublist for sublist_group in clean_data for sublist in sublist_group
    ]
    # print(clean_data)
    df = pd.DataFrame(flattened_list, columns=columns)
    df.to_csv("extracted_transactions.csv", index=False)
'''
