import openpyxl
import csv


data = openpyxl.load_workbook(filename="data.xlsx", data_only=True)
data = data[data.sheetnames[0]]

with open('output.csv', 'w') as csvfile:
    writer = csv.writer(
        csvfile, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in data:
        row = []
        for j in i:
            try:
                j = str(float(j))
            except ValueError:
                pass
            row.append(j)
        writer.writerow(row)
