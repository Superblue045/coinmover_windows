import sys
import csv


data_path = f"{sys.path[0]}\\domain\\"

# ex : fileName = bybit_symbols.csv
def get_file_data(fileName:str):
    file_data = open(f"{data_path}{fileName}")
    reader = csv.reader(file_data)
    next(reader)
    return reader
