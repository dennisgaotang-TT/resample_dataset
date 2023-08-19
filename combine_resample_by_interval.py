import pandas as pd
import glob
import os
import gzip
from datetime import datetime, timedelta
from multiprocessing import Pool

# user-specified parameters, make sure these values are correct before execution
input_folder = '/Users/tanggao/Desktop/projects/derivative_tickers_binance_BTCUSDT/'
output_file = '/Users/tanggao/Desktop/projects/derivative_tickers_binance_BTCUSDT/output_combined.csv.gz'
resample_interval = 8 * 60 * 60 * 10**6  # 8 hours in microseconds
assert_not_na_columns = ['funding_rate', 'last_price']
dtype = {"exchange": str, "symbol": str, "timestamp": int, "local_timestamp": int, "funding_timestamp": str, "funding_rate":str, "predicted_funding_rate":str, "open_interest":str, "last_price":str, "index_price":str, "mark_price":str }

def process_file(input_file):
    with gzip.open(input_file, 'rt') as f:
        df = pd.read_csv(f, dtype=dtype)
        df['timestamp_readble'] = pd.to_datetime(df['timestamp'], unit='us')  # Convert to datetime
        # df['original_micros'] = df['timestamp'].view('int64') 
        df = remove_first_rows_with_na_value(df, assert_not_na_columns)
        # option to remove the empty value column

        resampled_df = df.resample(f'{resample_interval}us', on='timestamp_readble').first().reset_index()
        resampled_df['timestamp_match'] = pd.to_datetime(resampled_df['timestamp'], unit='us')  # Convert to datetime
        print("%s lines has been taken from file: %s" % (resampled_df.shape[0], input_file))
        # print("*************"*3)
        return resampled_df

def remove_first_rows_with_na_value(df, columns_to_check):
    # Drop initial rows until encountering a row with all columns A, B, C, and D not N/A
    mask = df[columns_to_check].notna().all(axis=1)
    first_valid_index = mask.idxmax()  # Index of the first row meeting the condition
    df_after_remove_head_lines = df.iloc[first_valid_index:]
    return df_after_remove_head_lines
    
def combine_data(resampled_data):
    # Sort the DataFrames based on the original_micros column before concatenating
    sorted_data = sorted(resampled_data, key=lambda df: df['timestamp_readble'][0])
    # Check whether the time is connected
    # Check for consecutive dates
    
    prev_date = None
    for df in sorted_data:
        curr_date = df['timestamp_readble'][0]
        if prev_date is not None and (curr_date - prev_date).days > 1:
            print(f"Missing dates between {prev_date} and {curr_date}")
            # Handle missing dates here if needed
            raise("No File Error: lacking of files between (date {}, date {})".format(prev_date, curr_date))
        prev_date = curr_date

    combined_data = pd.concat(sorted_data)
    combined_data.to_csv(output_file, index=False)#, compression='gzip')

if __name__ == '__main__':
    input_files = glob.glob(os.path.join(input_folder, '*.csv.gz'))
    
    sorted_map = {}
    
    num_processes = min(len(input_files), os.cpu_count())
    
    with Pool(num_processes) as pool:
        resampled_data = pool.map(process_file, input_files)
        
    combine_data(resampled_data)
    
    print("Resampling and combining completed.")
