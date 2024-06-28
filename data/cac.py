import csv

# File paths
source_file = 'plagiarism.csv'
destination_file = 'plagiarism(2).csv'

# Copy content from source to destination
with open(source_file, 'r', newline='', encoding='utf-8') as src:
    reader = csv.reader(src)
    with open(destination_file, 'w', newline='', encoding='utf-8') as dst:
        writer = csv.writer(dst)
        writer.writerow(["text", "label"])
        for row in reader:
            writer.writerow(row)