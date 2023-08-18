# combine_resample_by_interval.py

## 0. what this program does: 
  * input: a folder containing consecutive .csv.gz files, for each we need to take out several rows by resampling by time intervals
  * output: a .csv.gz file combining all the rows taken out from each file in time order
  * This program might not need to be used on "derivative_ticker" dataset type. It can be used to resample any .csv.gz files containing a "timestamp" column if we corretly set the below user-specified parameters.
  * The number of rows taken out for each file depends on the resample interval and the intervals are started from 00:00:00 each day.
  * The program utilized multiprocessing to resample each file parallely and stored in the list. The list is then sorted and being combined into one output file.
    
## 1.before execusion: Remember to edit the file and set the below listed configurable parameters
* **input_folder**: str - the full path of the input folder containing all consecutive-date .csv.gz files for a symbol(pair)
* **output_file**: str - the full path of the output .csv.gz file name specifying the location we want the output file to be
* **resample_interval**: int - the resample interval in us(microseconds), for example an 8-hr interval will be "8 * 60 * 60 * 10**6  # 8 hours in microseconds"; an 8-hr interval will result in ideally 3 lines for each one-day input file
* **assert_not_na_columns**: list of strings - the column names for the program to remove the first few lines of each input file until it encountered a line where the values in assert_not_na_columns are all non-na values. This parameter is useful when users want to get some columns for later usage in the resample process 
* **dtype**: {key=str : values = python-dtype }- This dtype parameter is passed into the pd.read_csv() function for converting .csv.gz file into pandas dataframe object. The user might need to specify certain column's dtype for a deterministic state of data type convertion. For example, if this dtype is not specified, the values in the "funding rate" column(float) might be represented in scientific notation like 10e-3, which will being outputed into the output .csv.gz. We want to keep the original number during the resample process. So it is better to specify "funding_rate":str.
  
## 2.execute the program by cmd: 'python3 combine_resample_by_interval.py' after editing the above parameters/arguments
* make sure pandas is installed before execution: "pip install pandas"
