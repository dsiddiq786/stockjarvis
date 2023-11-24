import os
import pandas as pd
from datetime import datetime, timedelta

""" 
    Step No 2:  (Manuplate the Data)
    Author : Dawood Siddiq
    Description : Add missing seconds rows in all provided datasets . Pick last row before missing seconds and add same row on current second.
"""


def add_missing_seconds(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    csv_files = [file for file in os.listdir(input_folder) if file.startswith('cleaned_') and file.endswith('.csv')]

    for file in csv_files:
        df = pd.read_csv(os.path.join(input_folder, file))

        # Convert 'Time' column to datetime format
        df['Time'] = pd.to_datetime(df['Time'])

        # Get the minimum and maximum time in the dataset
        min_time = df['Time'].min()
        max_time = df['Time'].max()

        # Create a time range from minimum to maximum time
        time_range = pd.date_range(start=min_time, end=max_time, freq='S')

        # Create a DataFrame with the complete time range
        complete_df = pd.DataFrame({'Time': time_range})

        # Merge the original data with the complete time range data
        merged_df = pd.merge(complete_df, df, on='Time', how='left')

        # Forward-fill missing values for other columns (seconds)
        merged_df.fillna(method='ffill', inplace=True)

        # Save the file with complete time sequence to the output folder
        output_path = os.path.join(output_folder, f"complete_{file[8:]}")
        merged_df.to_csv(output_path, index=False)

input_folder_path = './cleaned_data'
output_folder_path = './complete_data'

add_missing_seconds(input_folder_path, output_folder_path)
