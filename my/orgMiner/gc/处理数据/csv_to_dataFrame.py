def csv_to_dataFrame(file):
    import csv
    import pandas as pd

    tmp_lst = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            tmp_lst.append(row)
    df = pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
    return df