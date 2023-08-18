import gzip
import glob
from datetime import datetime

# Folder containing date.csv.gz files
folder_path = "/Users/tanggao/Desktop/projects/derivative_tickers_binance_BTCUSDT/"

# List to store last lines
last_lines = []

# Identify all .csv.gz files in the folder
csv_files = glob.glob(folder_path + "*.csv.gz")
# Iterate through each file
for csv_file in csv_files:
    with gzip.open(csv_file, 'rt') as f:
        last_line = None
        for line in f:
            last_line = line.strip()
        if last_line:
            print(last_line)
            last_lines.append(last_line)
    
# Path for the combined file
combined_file_path = "/Users/tanggao/Desktop/projects/derivative_tickers_binance_BTCUSDT/combined_file.csv.gz"

# Write the combined last lines to the new file
with gzip.open(combined_file_path, 'wt') as f:
    for line in last_lines:
        f.write(line + '\n')
