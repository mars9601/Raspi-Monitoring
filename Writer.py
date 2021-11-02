import csv

with open ("plot.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["col1","col2","col3"])