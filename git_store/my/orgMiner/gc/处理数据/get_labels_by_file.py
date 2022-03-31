def get_labels_by_file(ogs_file):
    labels = []
    with open(ogs_file, 'r') as f:
        import csv
        reader = csv.reader(f)
        for row in reader:
            for i in range(len(row)):
                labels.append(int(row[i]))
    return labels